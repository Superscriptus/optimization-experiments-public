"""
Script to run stage 1 of experiment.

StateSpaceRespesentations are loaded from test_data/<data_dir> and are used to setup team allocation
tasks to be tested with each optimiser. The results are saved in stage_1_results/<experiment_name>

Note: results overview are logged to wandb.ai as well as being stored locally in full.
"""
import wandb
import os
import pickle
import time
from copy import deepcopy

import yaml
from pathlib import Path

from superscript_abm.model import SuperScriptModel
from superscript_abm.optimisation_decoupled import StateSpaceRepresentation, OptimiserFactory
from superscript_abm.utilities import Random

RUN_ID = 1
FILTER_SIZE = 100  # Number of workers to reduce workforce to
FILTER_TYPE = 'first_n'  # using this type of filter

data_to_use = 'validation_dataset_1'
run_name = data_to_use + '_run_%d' % RUN_ID
data_dir = Path('test_data') / data_to_use
results_dir = Path('stage_1_results/') / run_name

optimiser_types = [
    'greedy',
    'random',
    # 'exhaustive_search',
    # 'basin_hopping'
]

# TODO: add more save variables (e.g. team properties)
results = {
    optimiser_type: {
        'runtime': [],
        'probability': [],
        'team_size': [],
        'workers': [],
        'state_file': []
    }
    for optimiser_type in optimiser_types
}


def build_wandb_log_dict_and_results_dict(
        _results,
        _wandb_log_dict,
        _optimiser_type,
        _runtime,
        _probability,
        _team_size,
        _workers,
        _state_file_name
):
    _results[_optimiser_type]['runtime'].append(_runtime)
    _results[_optimiser_type]['probability'].append(_probability)
    _results[_optimiser_type]['team_size'].append(_team_size)
    _results[_optimiser_type]['workers'].append(_workers)
    _results[_optimiser_type]['state_file'].append(_state_file_name)

    _wandb_log_dict[_optimiser_type + '_runtime'] = _runtime
    _wandb_log_dict[_optimiser_type + '_probability'] = _probability
    _wandb_log_dict[_optimiser_type + '_team_size'] = _team_size
    _wandb_log_dict[_optimiser_type + '_workers'] = _workers
    _wandb_log_dict[_optimiser_type + '_state_file_name'] = _state_file_name


if __name__ == '__main__':

    os.makedirs(results_dir, exist_ok=False)
    files = Path(data_dir).glob('*.pickle')

    wandb.init(
        project="stage-1-test-run",
        name=run_name,
        config={
            "data": data_to_use,
            "data_dir": data_dir,
            "results_dir": results_dir,
            "filter_size": FILTER_SIZE,
            "filter_type": FILTER_TYPE
        }
    )

    optimiser_factory = OptimiserFactory()

    for fi, file in enumerate(files):

        state_file_name = os.path.basename(file)
        print("Running optimisation %d for: " % fi, state_file_name)
        wandb_log_dict = {}

        with open(file, 'rb') as in_file:
            state = pickle.load(in_file)

        state.config['optimisers']['exhaustive_search'] = {
            'team_size': 3,
            'timeout': 60
        }
        state.config['filters'][FILTER_TYPE] = {
            'filter_size': FILTER_SIZE
        }
        worker_filter = optimiser_factory.get_filter(FILTER_TYPE, state)
        worker_filter.filter()

        for optimiser_type in optimiser_types:

            this_state = deepcopy(state)
            assert this_state.state['worker_hard_skill_assignments'].sum() == 0

            try:
                optimiser = optimiser_factory.get_optimiser(
                    optimiser_type, this_state
                )
                solution = optimiser.solve()
                runtime = solution.runtime
                probability = solution.probability
                team_size = solution.team_size
                workers = solution.y.nonzero()[0]
            except:
                runtime = None
                probability = None
                team_size = None
                workers = None

            build_wandb_log_dict_and_results_dict(
                _results=results,
                _wandb_log_dict=wandb_log_dict,
                _optimiser_type=optimiser_type,
                _runtime=runtime,
                _probability=probability,
                _team_size=team_size,
                _workers=workers,
                _state_file_name=state_file_name

            )
        wandb.log(wandb_log_dict)
        if fi > 2:
            break

    print(results)

    with open(results_dir / 'results.pickle', 'wb') as out_file:
        pickle.dump(results, out_file)

    wandb.finish()
