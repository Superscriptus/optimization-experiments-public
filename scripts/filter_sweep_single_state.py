"""
Script to run a sweep across different filter sizes for a given filter, a single algorithm, and a single state.
"""
# TODO: refactor this script to be a generic experiment runner...
# TODO: remove debug print statements from here and optimisation_decoupled
import os
import sys
import pickle
import confuse
import numpy as np
from copy import deepcopy

from pathlib import Path

from superscript_abm.optimisation_decoupled import OptimiserFactory
from superscript_abm.project import NewSuccessCalculator
from experiment_configs.filter_sweep_single_state_config import CONFIG


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


if __name__ == '__main__':

    EXP_ID = int(sys.argv[1])  # experiment ID, corresponding to key in CONFIG
    RUN_ID = int(sys.argv[2])  # run ID, unique integer repeat counter for this experiment ID
    EXP_CONFIG = CONFIG[EXP_ID]

    os.makedirs(EXP_CONFIG['SAVE_TO'], exist_ok=True)

    data_path = EXP_CONFIG['DATASET']
    results_path = EXP_CONFIG['SAVE_TO'] / f"exp_{EXP_ID}_run_{RUN_ID}"
    os.makedirs(results_path, exist_ok=False)

    results = {
        fs: {
            'probability': [],
            'runtime': [],
            'team_size': [],
            'solution': []
        }
        for fs in EXP_CONFIG['FILTER_SIZES']
    }

    files = Path(data_path).glob('*.pickle')
    state_file = [
        os.path.basename(file)
        for fi, file in enumerate(files)
        if (
                int(os.path.basename(file).split('.')[0].split('_')[1])
                == EXP_CONFIG['STATE_ID']
        )
    ][0]

    print("Running optimisation for: ", state_file)
    with open(Path(__file__).parent / 'test_state_100_workers.pickle', 'rb') as in_file:
    #with open(data_path / state_file, 'rb') as in_file:
        state = pickle.load(in_file)

    # Now we configure the Optimiser
    optimiser_factory = OptimiserFactory()
    config = confuse.Configuration('SuperScriptModel', read=False)
    config.set_file(
        Path(__file__).parent / EXP_CONFIG['ABM_CONFIG_FILE'],
        base_for_paths=True
    )
    config.read()
    config['organisation_strategy']['filter_type'] = [EXP_CONFIG['FILTER_TYPE']]

    filter_type = EXP_CONFIG['FILTER_TYPE']
    print("OPT: ", EXP_CONFIG['OPTIMISER'])
    if EXP_CONFIG['OPTIMISER'] == 'reinforcement_learning':
        config['optimisers']['reinforcement_learning'] = {
            'trained_model': 'RLD2-v2.38_1', 
            'hyperparameters': 'RLD2-v2.38',
            'deterministic': False, 
            'num_repeats': EXP_CONFIG['RL_N_REPEAT_SOLUTIONS'],
        }

    for fs in EXP_CONFIG['FILTER_SIZES']:
        print("FS: ", fs)
        config['filters'][filter_type] = {
            'filter_size': fs
        }
        this_state = deepcopy(state)
        this_state.config = config
        filter_indices = None  # not using index filter here

        assert this_state.state['worker_hard_skill_assignments'].sum() == 0

        optimiser = optimiser_factory.get_optimiser(
            EXP_CONFIG['OPTIMISER'], this_state,
            filter_indices=filter_indices
        )
        print("OS_FS: ", optimiser.config['filters'][filter_type]['filter_size'])
        runner = optimiser_factory.get_runner(EXP_CONFIG['RUNNER'], optimiser)
        solution = runner.run()

        results[fs]['probability'].append(solution.probability)
        results[fs]['team_size'].append(solution.team_size)
        results[fs]['solution'].append(solution)
        results[fs]['runtime'].append(solution.runtime)
    #     components = get_probability_components(config, solution)

    print(results)

    with open(results_path / 'results.pickle', 'wb') as out_file:
        pickle.dump(results, out_file)


