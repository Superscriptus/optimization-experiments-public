"""
Script to produce test dataset for comparison of optimisation methods (stage 1 of experiment).

SuperScript ABM is created and run for a random number of timesteps. A StateSpaceRespesentation
is then created using the current workforce state and most recently created project. This representation
is saved to disk. We repeat N times. We also save the ABM configuration file for reference.
"""
import os
import pickle
import time
import yaml
from pathlib import Path

from superscript_abm.model import SuperScriptModel
from superscript_abm.optimisation_decoupled import StateSpaceRepresentation
from superscript_abm.utilities import Random

# Number of distinct states to produce:
N = 100
# Setting global config params to override config.yaml in constructor.
config_file = 'scripts/stage_1_config.yaml'
OVERRIDE_CONFIG = {
    #'io_dir': '/media/storage/rusty_data/superscript/ss_abm_datasets/10', 
    # 'io_dir': 'test_data/dataset_1',
    'io_dir': 'test_data/validation_dataset',
    'worker_count': 100,
    'department_count': 10,
    'new_projects_per_timestep': 2,
    'departmental_workload': 0.1,
    'optimiser_type': 'random',
    'runner_type': 'series',
    'data_collection': False,
    'save_projects': False,
    'load_projects': False,
    'save_network': False,
    'random_seed': None # 42
}


def create_and_run_model(simulation_timesteps, config_file):

    start_time = time.time()
    abm = SuperScriptModel(
        config_file=config_file,
        **OVERRIDE_CONFIG
    )

    abm.run_model(simulation_timesteps)
    elapsed_time = time.time() - start_time
    print(
        "Simulation completed %d timesteps in %.2f seconds."
        % (simulation_timesteps, elapsed_time)
    )

    return abm


if __name__ == '__main__':

    simulation_io_directory = Path(OVERRIDE_CONFIG['io_dir'])
    os.makedirs(simulation_io_directory, exist_ok=False)

    rngr = Random(seed=OVERRIDE_CONFIG['random_seed'])

    for i in range(N):
        print("Producing state %d:" % i)

        success = False
        while not success:
            try:

                abm = create_and_run_model(
                    simulation_timesteps=rngr.randint(1, 100),
                    config_file=config_file
                )
                pid, project = abm.inventory.projects.popitem()
                success = True
            except KeyError:
                print("Project creation failed.")

        if i == 0:
            yaml_out = yaml.safe_load(abm.config.dump())
            with open(simulation_io_directory / 'config.yaml', 'w') as out_file:
                yaml.dump(yaml_out, out_file)


        state = StateSpaceRepresentation(abm, project)
        # The project has been allocated a team in the ABM, so we remove this in the state:
        state.update_with_new_assignment()

        with open(simulation_io_directory / ('state_%d.pickle' % i), 'wb') as out_file:
            pickle.dump(state, out_file)


