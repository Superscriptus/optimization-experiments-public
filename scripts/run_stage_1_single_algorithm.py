"""
Script to run stage 1 of experiment.

This version just runs for a single algorithm - this provides a nicer view on wandb
where we can compare graphically across runs.

StateSpaceRespesentations are loaded from test_data/<data_dir> and are used to setup team allocation
tasks to be tested with each optimiser. The results are saved in stage_1_results/single_algorithm/<experiment_name>

We introduce here the option of using an index filter based on a previous solution, to reduce the
problem size. This is mainly intended to be used by exhaustive_search to index_filter on Greedy solution. The
effect of this is to see if there is a better hard_skill allocation for those workers.

Note: results overview are logged to wandb.ai as well as being stored locally in full.

Refactor note (Stage 1 cleanup, issue #4): the experiment is now exposed as the callable
``run_stage1(...)`` so that it can be driven from tests/other code without subprocessing. The
``__main__`` block below preserves the original behaviour exactly (same GLOBALS, same paths,
no random seeding, wandb left commented out).
"""
import wandb
import os
import pickle
import confuse
import numpy as np
from copy import deepcopy

from pathlib import Path

from superscript_abm.optimisation_decoupled import OptimiserFactory
from superscript_abm.project import NewSuccessCalculator

# TODO: add different modes for HRL
# TODO: remove parallel wall_timeout?
# TODO: implement and test other filter types

# Note: when running for RLD2, filtering does not work very well because the agent has not been trained for a reduced
# number of workers. It is best to use a model that has been trained on a filtered workforce (i.e. RLD2_FILTERED).
# To do this: input the required FILTER_SIZE in GLOBALS but leave the FILTER_TYPES list empty.

# Default experiment configuration (was the module-level GLOBALS dict). The __main__ block uses
# these values unchanged; callers of run_stage1() can override any subset via globals_overrides.
DEFAULT_GLOBALS = {
    'RUN_ID': 3029,
    'FILTER_SIZE': 100,  # Number of workers to reduce workforce to
    'FILTER_TYPES': ['ml_filter'],  # ['index']  # If using 'index' only FILTER_SIZE is not used and indices are loaded from:
    'LOAD_INDICES_FROM': None,# Path('stage_1_results/single_algorithm/stage_1_100_projects_100_workers_nonlinear/dataset_1_grasp_run_0/results.pickle'),
    'OPTIMISER_TYPE': 'ensemble',  # 'rld2_1000_10', #'greedy',
    'RUNNER_TYPE': 'series',
    'OBJECTIVE': 'nonlinear'  # whether to use linear or nonlinear components of probability function
}

DEFAULT_DATA_TO_USE = 'test_dataset'  # 'test_dataset' #'example_dataset'


def _resolve_model_and_rl_config(GLOBALS):
    """Reproduce the original module-level model-selection / RL-config logic.

    Mutates GLOBALS in place exactly as the original script did (e.g. mapping the 'rld2*'
    optimiser aliases onto 'reinforcement_learning' and adjusting RUNNER_TYPE), and returns
    the rl_config_dict (or None for non-RL optimisers).
    """
    model_name = None
    model_env = None

    # Handles using pretrained RLD2_FILTERED instead of filtering state for a 100 RLD2 (described above)
    if GLOBALS['FILTER_SIZE'] < 100 and 'rld2' in GLOBALS['OPTIMISER_TYPE'] and len(GLOBALS['FILTER_TYPES']) == 0:
        # model_name = f"RLD2_{GLOBALS['FILTER_SIZE']}-v1_18"
        # model_env = f"RLD2_{GLOBALS['FILTER_SIZE']}-v1"
        model_name = f"RLD2_{GLOBALS['FILTER_SIZE']}-v1.62-{GLOBALS['OBJECTIVE']}_1"
        model_env = f"RLD2_{GLOBALS['FILTER_SIZE']}-v1.62-{GLOBALS['OBJECTIVE']}"
    elif 'rld2' in GLOBALS['OPTIMISER_TYPE'] and GLOBALS['OBJECTIVE'] == 'linear':
        model_name = 'RLD2-v3.106-linear_1'
        model_env = 'RLD2-v3.106-linear'
    elif 'rld2' in GLOBALS['OPTIMISER_TYPE'] and GLOBALS['OBJECTIVE'] == 'nonlinear':
        model_name = 'RLD2-v3.106-nonlinear_2'
        model_env = 'RLD2-v3.106-nonlinear'

    # add configuration that is specific to the various HRL modes
    if GLOBALS['OPTIMISER_TYPE'] == 'rld2':
        rl_config_dict = {
            'trained_model': model_name,
            'hyperparameters': model_env,
            'deterministic': True,
            'num_repeats': 1,
            'rld1_deterministic': True,
            'rld1_num_repeats': 1,
            'timeout': 1
        }
        GLOBALS['OPTIMISER_TYPE'] = 'reinforcement_learning'
    elif GLOBALS['OPTIMISER_TYPE'] == 'rld2_100_10':
        rl_config_dict = {
            'trained_model': model_name,
            'hyperparameters': model_env,
            'deterministic': False,
            'num_repeats': 1, #10, CHANGE
            'rld1_deterministic': False,
            'rld1_num_repeats': 1, # 10, CHANGE
            'timeout': 1
        }
        GLOBALS['OPTIMISER_TYPE'] = 'reinforcement_learning'
        GLOBALS['RUNNER_TYPE'] = 'parallel'
    elif GLOBALS['OPTIMISER_TYPE'] == 'rld2_1000_10':
        rl_config_dict = {
            'trained_model': model_name,
            'hyperparameters': model_env,
            'deterministic': False,
            'num_repeats': 100,
            'rld1_deterministic': False,
            'rld1_num_repeats': 10,
            'timeout': 1
        }
        GLOBALS['OPTIMISER_TYPE'] = 'reinforcement_learning'
        GLOBALS['RUNNER_TYPE'] = 'parallel'
    elif GLOBALS['OPTIMISER_TYPE'] == 'ensemble':
        assert GLOBALS['FILTER_SIZE'] == 100  # Currently assuming this for Ensemble solver.
        model_name = f"RLD2_20-v1.62-{GLOBALS['OBJECTIVE']}_1"
        model_env = f"RLD2_20-v1.62-{GLOBALS['OBJECTIVE']}"
        rl_config_dict = {
            'trained_model': model_name,
            'hyperparameters': model_env,
            'deterministic': False,
            'num_repeats': 10,
            'rld1_deterministic': False,
            'rld1_num_repeats': 10,
            'timeout': 1
        }
        GLOBALS['OPTIMISER_TYPE'] = 'ensemble'
        GLOBALS['RUNNER_TYPE'] = 'series'
    elif GLOBALS['OPTIMISER_TYPE'] == 'greedy_rl':
        model_name = 'RLD2-v3.106-nonlinear_2'
        model_env = 'RLD2-v3.106-nonlinear'
        assert GLOBALS['FILTER_SIZE'] == 100  # Currently assuming this for Greedy RL solver.
        rl_config_dict = {
            'trained_model': model_name,
            'hyperparameters': model_env,
            'deterministic': False,
            'num_repeats': 10,
            'rld1_deterministic': False,
            'rld1_num_repeats': 10,
            'timeout': 1
        }
        GLOBALS['RUNNER_TYPE'] = 'series'
    else:
        rl_config_dict = None

    return rl_config_dict


def _new_results_dict():
    return {
            'runtime': [],
            'probability': [],
            'team_size': [],
            'workers': [],
            'state_file': [],
            'timeout': [],
            'ovr': [],
            'skill_balance': [],
            'creativity_match': [],
            'creativity_level': [],
            'risk': [],
            'individual_chemistry': [],
            'team_chemistry': [],
            'probability_ovr': [],
            'probability_skill_balance': [],
            'probability_creativity_match': [],
            'probability_individual_chemistry': [],
            'probability_team_chemistry': [],
            'probability_risk': [],
            'solution_x': []
    }


def build_wandb_log_dict_and_results_dict(
        _results,
        _wandb_log_dict,
        **kwargs
):
    for arg, value in kwargs.items():
        _results[arg].append(value)
        _wandb_log_dict[arg] = value


def load_filter_indices(state_file_name, previous_results=None):
    if previous_results is not None:
        return previous_results['workers'][
            previous_results['state_file'].index(state_file_name)
        ]
    else:
        return []


def get_probability_components(config, solution):

    calculator = NewSuccessCalculator(
        config=config,
        project=None,
        network=None,
        component_values={
            'ovr': solution.state.team_ovr,
            'skill_balance': solution.state.skill_balance,
            'creativity_match': solution.state.creativity_match,
            'risk': solution.state.risk,
            'individual_chemistry': solution.state.individual_chemistry,
            'team_chemistry': solution.state.team_chemistry
        }
    )
    return {
       'probability_ovr': calculator.probability_ovr,
       'probability_skill_balance': calculator.probability_skill_balance,
       'probability_creativity_match': calculator.probability_creativity_match,
       'probability_individual_chemistry': calculator.probability_individual_chemistry,
       'probability_team_chemistry': calculator.probability_team_chemistry,
       'probability_risk': calculator.probability_risk
    }


def initialise_wandb(data_dir, run_name, project_name, config_fs, load_indices_from=None):
    run = wandb.init(
        name=run_name,
        project=project_name,
        config=config_fs
    )
    artifact = wandb.Artifact(name='run_data', type='dataset')
    artifact.add_dir(local_path=data_dir)
    run.log_artifact(artifact)
    artifact = wandb.Artifact(name='run_scripts', type='scripts')
    artifact.add_dir(local_path=Path(__file__).parent)
    run.log_artifact(artifact)
    if load_indices_from is not None:
        artifact = wandb.Artifact(name='load_indices_from', type='prior_results')
        artifact.add_dir(local_path=load_indices_from.parent)
        run.log_artifact(artifact)


def run_stage1(
        globals_overrides=None,
        *,
        data_to_use=DEFAULT_DATA_TO_USE,
        config_path=None,
        data_dir=None,
        results_dir=None,
        random_seed=None,
        make_results_dir=True,
        write_results=True,
        use_wandb=False,
):
    """Run stage 1 (single algorithm) over every state in ``data_dir`` and return the results dict.

    Parameters
    ----------
    globals_overrides : dict, optional
        Overrides applied on top of DEFAULT_GLOBALS (e.g. {'OPTIMISER_TYPE': 'greedy'}).
    data_to_use : str
        Subfolder of test_data/ to load states from (used to derive default paths/names).
    config_path : Path, optional
        Path to the ABM/optimiser YAML config. Defaults to scripts/stage_1_config.yaml.
    data_dir : Path, optional
        Directory of state pickles to solve. Defaults to test_data/<data_to_use>.
    results_dir : Path, optional
        Where to write results.pickle. Defaults to the original derived path.
    random_seed : int, optional
        If set, written into the config as random_seed (used for deterministic regression
        runs). Defaults to None, which leaves the config's own value untouched — preserving
        the original (unseeded) __main__ behaviour.
    make_results_dir : bool
        Whether to create results_dir (os.makedirs exist_ok=False, as in the original).
    write_results : bool
        Whether to pickle the results to results_dir.
    use_wandb : bool
        Whether to initialise and log to wandb (the original had this commented out -> False).

    Returns
    -------
    dict
        The populated results dictionary.
    """
    GLOBALS = deepcopy(DEFAULT_GLOBALS)
    if globals_overrides:
        GLOBALS.update(globals_overrides)

    run_name = data_to_use + '_%s_final_run_%d' % (GLOBALS['OPTIMISER_TYPE'], GLOBALS['RUN_ID'])
    project_name = f"stage_1_{data_to_use}_{GLOBALS['FILTER_SIZE']}_workers_{GLOBALS['OBJECTIVE']}"
    if config_path is None:
        config_path = Path(__file__).parent / 'stage_1_config.yaml'
    if data_dir is None:
        data_dir = Path('test_data') / data_to_use
    if results_dir is None:
        results_dir = Path('stage_1_results/single_algorithm') / project_name / run_name

    # Remove any filter if not needed:
    if GLOBALS['FILTER_SIZE'] == 100:
        GLOBALS['FILTER_TYPES'] = []

    rl_config_dict = _resolve_model_and_rl_config(GLOBALS)

    results = _new_results_dict()

    if make_results_dir:
        os.makedirs(results_dir, exist_ok=False)
    files = Path(data_dir).glob('*.pickle')

    try:
        with open(GLOBALS['LOAD_INDICES_FROM'], 'rb') as in_file:
            previous_results = pickle.load(in_file)
    except:
        previous_results = None

    optimiser_factory = OptimiserFactory()
    config = confuse.Configuration('SuperScriptModel', read=False)
    config.set_file(config_path, base_for_paths=True)
    config.read()

    if random_seed is not None:
        config['random_seed'] = random_seed

    filt_dict = config['filters'].get()
    filt_dict['first_n'] = {
        'filter_size': GLOBALS['FILTER_SIZE']
    }
    filt_dict['random'] = {
        'filter_size': GLOBALS['FILTER_SIZE']
    }
    filt_dict['ml_filter'] = {
        'filter_size': GLOBALS['FILTER_SIZE'],
        'model_file': 'rf_trained_cv.joblib',
        'n_jobs': 1
    }
    config['filters'] = filt_dict

    if rl_config_dict is not None:
        opt_dict = config['optimisers'].get()
        opt_dict['reinforcement_learning'] = rl_config_dict
        config['optimisers'] = opt_dict

    proj_dict = config['project'].get()
    proj_dict['success_probability_calculator_type'] = f"weighted_{GLOBALS['OBJECTIVE']}"
    config['project'] = proj_dict

    config_fs = dict(config)
    config_fs['results_dir'] = results_dir
    for key in GLOBALS.keys():
        config_fs[key] = GLOBALS[key]

    if use_wandb:
        initialise_wandb(data_dir, run_name, project_name, config_fs,
                         load_indices_from=GLOBALS['LOAD_INDICES_FROM'])

    for fi, file in enumerate(files):
        state_file_name = os.path.basename(file)
        # if state_file_name =="state_13.pickle":
        if True:

            print("Running optimisation %d for: " % fi, state_file_name)
            wandb_log_dict = {}

            with open(file, 'rb') as in_file:
                state = pickle.load(in_file)

            this_state = deepcopy(state)
            this_state.config = config

            filter_indices = load_filter_indices(state_file_name, previous_results=previous_results)

            opt_dict = config['optimisers'].get()
            opt_dict['exhaustive_search'] = {
                'timeout': 36000,
                'team_size': len(filter_indices)
            }
            config['optimisers'] = opt_dict

            org_dict = this_state.config['organisation_strategy'].get()
            org_dict['filter_type'] = GLOBALS['FILTER_TYPES']
            this_state.config['organisation_strategy'] = org_dict

            assert this_state.state['worker_hard_skill_assignments'].sum() == 0

            optimiser = optimiser_factory.get_optimiser(
                GLOBALS['OPTIMISER_TYPE'], this_state,
                filter_indices=filter_indices
            )
            runner = optimiser_factory.get_runner(GLOBALS['RUNNER_TYPE'], optimiser)
            solution = runner.run()
            components = get_probability_components(config, solution)

            build_wandb_log_dict_and_results_dict(
                _results=results,
                _wandb_log_dict=wandb_log_dict,
                state_file=state_file_name,
                runtime=solution.runtime,
                probability=solution.probability,
                team_size=solution.team_size,
                workers=solution.y.nonzero()[0],
                timeout=int(solution.timeout),
                ovr=solution.state.team_ovr,
                skill_balance=solution.state.skill_balance,
                creativity_match=solution.state.creativity_match,
                creativity_level=solution.state.creativity_level,
                risk=solution.state.risk,
                individual_chemistry=solution.state.individual_chemistry,
                team_chemistry=solution.state.team_chemistry,
                solution_x=solution.x,
                **components
                )
            if use_wandb:
                wandb.log(wandb_log_dict)

    if write_results:
        with open(results_dir / 'results.pickle', 'wb') as out_file:
            pickle.dump(results, out_file)

    if use_wandb:
        wandb.finish()

    return results


if __name__ == '__main__':
    run_stage1()
