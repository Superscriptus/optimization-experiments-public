"""
Script to run stage 2 of experiment.

This version just runs for a single algorithm.

Currently we use default parameter values for the ABM, which is simulated REP_ABM times to produce
a set of results for a single algorithm.
(In future we will conduct sensitivity anlyses with different parameter values.)

An initial run is done with the ORandom optimiser, and this run saves the projects in io_dir
for use by subsequent runs. This reuse of projects allows for a fairer comparison between
different team allocation methods when using a small number of repeats (REP_ABM). For subsequent runs,
the projects are loaded from LOADS_PROJECTS_FROM, from the corresponding repeat_<id> directory.

The results are saved in stage_2_results/single_algorithm/<experiment_name>/<repeat_number>
And this is also used as the ABM io_dir.

Note: results overview are logged to wandb.ai as well as being stored locally in full.
"""
import pickle
import shutil
import os
import time
from pathlib import Path

from superscript_abm.model import SuperScriptModel
from superscript_abm.project import NewSuccessCalculator


# Note: when running for RLD2, filtering does not work very well because the agent has not been trained for a reduced
# number of workers. It is best to use a model that has been trained on a filtered workforce (i.e. RLD2_FILTERED).
# To do this: input the required FILTER_SIZE in GLOBALS but leave the FILTER_TYPES list empty.
RESTART_FROM = 0

GLOBALS = {
    'RUN_ID': 2026,
    'REP_ABM': 30,  # Number of repeat ABM simulations to run
    'FILTER_SIZE': 20,  # Number of workers to reduce workforce to
    'FILTER_TYPES': ['ml_filter'],  # ['index']  # If using 'index' only FILTER_SIZE is not used and indices are loaded from:
    # 'LOAD_INDICES_FROM': Path('stage_1_results/single_algorithm/stage_1_100_projects_100_workers_nonlinear/dataset_1_grasp_run_0/results.pickle'),
    'LOAD_PROJECTS_FROM': Path(
        '/media/storage/rusty_data/superscript/optimization_experiments/stage_2_results/single_algorithm/stage_2_100_workers_nonlinear/random_run_0'
    ),
    'OPTIMISER_TYPE': 'ensemble',
    'RUNNER_TYPE': 'series',
    'OBJECTIVE': 'linear',  # whether to use linear or nonlinear components of probability function,
    'ABM_TIMESTEPS': 100,
    'ABM_CONFIG_FILE': 'scripts/stage_2_config.yaml',
    'SAVE_PROJECTS': False,
    'LOAD_PROJECTS': True
}

run_name = f"{GLOBALS['OPTIMISER_TYPE']}_run_{GLOBALS['RUN_ID']}"
project_name = f"stage_2_{GLOBALS['FILTER_SIZE']}_workers_{GLOBALS['OBJECTIVE']}"
results_dir = Path(
    # '/media/storage/rusty_data/superscript/optimization_experiments/stage_2_results/single_algorithm'
    '/media/data/rusty_data/stage_2_results/single_algorithm'

) / project_name / run_name

# Remove any filter if not needed:
if GLOBALS['FILTER_SIZE'] == 100:
    GLOBALS['FILTER_TYPES'] = []

# Handles using pretrained RLD2_FILTERED instead of filtering state for a 100 RLD2 (described above)
if GLOBALS['FILTER_SIZE'] < 100 and 'rld2' in GLOBALS['OPTIMISER_TYPE'] and len(GLOBALS['FILTER_TYPES']) == 0:
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
        'num_repeats': 10,
        'rld1_deterministic': False,
        'rld1_num_repeats': 10,
        'timeout': 1
    }
    GLOBALS['OPTIMISER_TYPE'] = 'reinforcement_learning'
    GLOBALS['RUNNER_TYPE'] = 'parallel'
elif GLOBALS['OPTIMISER_TYPE'] == 'rld2_100_1':
    rl_config_dict = {
        'trained_model': model_name,
        'hyperparameters': model_env,
        'deterministic': False,
        'num_repeats': 10,
        'rld1_deterministic': True,
        'rld1_num_repeats': 1,
        'timeout': 1
    }
    GLOBALS['OPTIMISER_TYPE'] = 'reinforcement_learning'
    GLOBALS['RUNNER_TYPE'] = 'parallel'
elif GLOBALS['OPTIMISER_TYPE'] == 'rld2_10':
    rl_config_dict = {
        'trained_model': model_name,
        'hyperparameters': model_env,
        'deterministic': False,
        'num_repeats': 10,
        'rld1_deterministic': True,
        'rld1_num_repeats': 1,
        'timeout': 1
    }
    GLOBALS['OPTIMISER_TYPE'] = 'reinforcement_learning'
    GLOBALS['RUNNER_TYPE'] = 'series'
elif GLOBALS['OPTIMISER_TYPE'] == 'ensemble':
    assert GLOBALS['FILTER_SIZE'] == 20  # Currently assuming this for Ensemble solver.
    model_name = f"RLD2_{GLOBALS['FILTER_SIZE']}-v1.62-{GLOBALS['OBJECTIVE']}_1"
    model_env = f"RLD2_{GLOBALS['FILTER_SIZE']}-v1.62-{GLOBALS['OBJECTIVE']}"
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
else:
    rl_config_dict = {}


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


def create_and_run_model(config_file, override_config, simulation_timesteps=100):

    start_time = time.time()
    abm = SuperScriptModel(
        config_file=config_file,
        **override_config
    )
    # print("ABM TA: ", abm.team_allocator.config['organisation_strategy'].get())
    # print("ABM TA: ", abm.team_allocator.config['runners'].get())
    # print("ABM TA: ", abm.team_allocator.config['optimisers']['reinforcement_learning'].get())
    abm.run_model(simulation_timesteps)
    elapsed_time = time.time() - start_time
    print(
        "Simulation completed %d timesteps in %.2f seconds."
        % (simulation_timesteps, elapsed_time)
    )

    return abm, elapsed_time


def save_tracking_data(data, directory, simulation_name='example', verbose=False):
    if verbose:
        print("Simulation: ", simulation_name)

    for data_name, data_item in data.items():

        if verbose:
            print("Dataframe head for " + data_name)
            print(data_item.head())

        with open(
                Path(directory, simulation_name + '_' + data_name + '.pickle'), 'wb'
        ) as outfile:

            pickle.dump(data_item, outfile)


def get_tracking_data(model):
    try:
        data = {
            'model_variables': model.datacollector.get_model_vars_dataframe(),
            'project_table': model.datacollector.get_table_dataframe('Projects'),
            'agent_variables': model.datacollector.get_agent_vars_dataframe()
        }
    except AttributeError as e:
        print(e)
        data = None

    return data

if __name__ == '__main__':

    os.makedirs(results_dir, exist_ok=False)

    # try:
    #     with open(GLOBALS['LOAD_INDICES_FROM'], 'rb') as in_file:
    #         previous_results = pickle.load(in_file)
    # except:
    #     previous_results = None

    simulation_timer = {}

    if GLOBALS['LOAD_PROJECTS']:
        assert not GLOBALS['SAVE_PROJECTS']

    base_config = {
        'worker_count': 100,
        'department_count': 10,
        'new_projects_per_timestep': 2,
        'departmental_workload': 0.1,
        'optimiser_type': GLOBALS['OPTIMISER_TYPE'],
        'runner_type': GLOBALS['RUNNER_TYPE'],
        'data_collection': True,
        'save_projects': GLOBALS['SAVE_PROJECTS'],
        'load_projects': GLOBALS['LOAD_PROJECTS'],
        'save_network': True
    }
    base_config['first_n'] = {
        'filter_size': GLOBALS['FILTER_SIZE']
    }
    base_config['random'] = {
        'filter_size': GLOBALS['FILTER_SIZE']
    }
    base_config['ml_filter'] = {
        'filter_size': GLOBALS['FILTER_SIZE'],
        'model_file': 'rf_trained_cv.joblib',
        'n_jobs': 1
    }
    base_config['success_probability_calculator_type'] = f"weighted_{GLOBALS['OBJECTIVE']}"

    # base_config['project']['success_probability_calculator_type'] = f"weighted_{GLOBALS['OBJECTIVE']}"
    if 'reinforcement_learning' in GLOBALS['OPTIMISER_TYPE']:
        base_config['reinforcement_learning'] = rl_config_dict

    # Was used previously for W&B...
    # config_fs = dict(base_config)
    # config_fs['results_dir'] = results_dir
    # for key in GLOBALS.keys():
    #     config_fs[key] = GLOBALS[key]

    for ri in range(GLOBALS['REP_ABM']):
        if ri >= RESTART_FROM:
            print("Running repeat ABM number %d" % ri)
            rep_dir = results_dir / f"repeat_{ri}"
            os.makedirs(rep_dir, exist_ok=False)

            if GLOBALS['LOAD_PROJECTS']:
                shutil.copyfile(
                    src=GLOBALS['LOAD_PROJECTS_FROM'] / f"repeat_{ri}/project_file.dill",
                    dst=rep_dir / "project_file.dill"
                )

            # wandb_log_dict = {}

            override_config = {
                'io_dir': str(rep_dir),
                'random_seed': ri
            }
            override_config.update(base_config)
            abm, elapsed_time = create_and_run_model(
                config_file=GLOBALS['ABM_CONFIG_FILE'],
                override_config=override_config,
                simulation_timesteps=GLOBALS['ABM_TIMESTEPS']
            )
            tracking_data = get_tracking_data(abm)
            save_tracking_data(tracking_data, rep_dir, simulation_name='abm_data')

            simulation_timer[f"repeat_{ri}"] = elapsed_time

    with open(results_dir / "simulation_times.pickle", 'wb') as outfile:
        pickle.dump(simulation_timer, outfile)
