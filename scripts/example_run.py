"""
Example script to run SuperScript ABM and save output.

The base configuration for the SuperScript model is read from config.py but we can override
the config parameters in the SuperScriptModel() constructor call, as below.

Project creation:
If load_projects=False, projects are created at random on each timestep
If load_projects=True, pre-defined projects are loaded from <io_dir>/project_file.pickle
If save_projects=True, the projects created during the simulation are saved to <io_dir>/project_file.pickle

Initial conditions:
In general the workforce is created at random when the constructor is called. We can seed the random number
generator by setting RANDOM_SEED in the config file or constructor call, such that the initial conditions
(and subsequent simulation, providing everything else is held constant) are the same. This is demonstrated below.

We can also copy an existing ABM using the method SuperScriptModel.copy_existing_abm(). This allows us to
continue a simulation from where it finished, or to restart a simulation using the same workforce state that
was produced by a previous one. This functionality is also demonstrated below.

Note: The simulation runs faster with data_collection=False but then we cannot access tracking data
after the simulation.

Note: this example must be run with config['optimisers']['random']['respect_constraints'] = False, otherwise
the results are non-deterministic (even with random seeding) due to the 'timeout' in the while loop that
attempts to meet the constraint by selection random teams (i.e. we don't know how many attempts will be made
during timeout).
"""
import os
import pickle
import time
import shutil
from pathlib import Path
from superscript_abm.model import SuperScriptModel

# Setting global config params to override config.py in constructor.
SIMULATION_TIMESTEPS = 100
SIMULATION_IO_DIRECTORY = Path('training_data/example_grasp_team_allocation')
WORKER_COUNT = 100
DEPARTMENT_COUNT = 10
PROJECTS_PER_TIMESTEP = 2
DEPARTMENTAL_WORKLOAD = 0.1
OPTIMISER_TYPE = 'random'  # 'basin'
RUNNER_TYPE = 'series'
DATA_COLLECTION = True
SAVE_PROJECTS = True
LOAD_PROJECTS = False
RANDOM_SEED = 42


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


def create_and_run_model(
        simulation_timesteps=SIMULATION_TIMESTEPS,
        simulation_io_directory=SIMULATION_IO_DIRECTORY,
        worker_count=WORKER_COUNT,
        department_count=DEPARTMENT_COUNT,
        projects_per_timestep=PROJECTS_PER_TIMESTEP,
        departmental_workload=DEPARTMENTAL_WORKLOAD,
        optimiser_type=OPTIMISER_TYPE,
        runner_type=RUNNER_TYPE,
        data_collection=DATA_COLLECTION,
        save_projects=SAVE_PROJECTS,
        load_projects=LOAD_PROJECTS,
        random_seed=RANDOM_SEED
):
    start_time = time.time()
    abm = SuperScriptModel(
        worker_count=worker_count,
        department_count=department_count,
        new_projects_per_timestep=projects_per_timestep,
        optimiser_type=optimiser_type,
        runner_type=runner_type,
        departmental_workload=departmental_workload,
        data_collection=data_collection,
        save_network=False,
        save_projects=save_projects,
        load_projects=load_projects,
        io_dir=str(simulation_io_directory),
        random_seed=random_seed
    )

    abm.run_model(simulation_timesteps)
    elapsed_time = time.time() - start_time
    print(
        "Simulation completed in %.2f seconds."
        % elapsed_time
    )

    tracking_data = get_tracking_data(abm)

    return abm, tracking_data


if __name__ == '__main__':

    os.makedirs(SIMULATION_IO_DIRECTORY, exist_ok=False)

    if LOAD_PROJECTS:
        shutil.copyfile(
            Path('training_data/example_project_file.pickle'),
            SIMULATION_IO_DIRECTORY / 'project_file.pickle'
        )

    abm_1, data_1 = create_and_run_model()
    save_tracking_data(data_1, SIMULATION_IO_DIRECTORY, 'base')

    # Here we create a model with the same random seed and config, and check that the outputs are the same:
    abm_2, data_2 = create_and_run_model()
    save_tracking_data(data_2, SIMULATION_IO_DIRECTORY, 'seed')

    for key in data_1.keys():
        assert data_1[key].equals(data_2[key]), print(key)

    # Now we copy the ABM from a completed simulation and restart it from time=0, using the same projects:
    abm_1 = SuperScriptModel.copy_existing_abm(
        abm_1,
        mode='restart',
        load_projects=True,
        save_projects=False,
        io_dir=SIMULATION_IO_DIRECTORY
    )
    abm_1.run_model(SIMULATION_TIMESTEPS)
    data_1 = get_tracking_data(abm_1)
    save_tracking_data(data_1, SIMULATION_IO_DIRECTORY, 'copy1', verbose=False)

    abm_2 = SuperScriptModel.copy_existing_abm(
        abm_2,
        mode='restart',
        load_projects=True,
        save_projects=False,
        io_dir=SIMULATION_IO_DIRECTORY
    )
    abm_2.run_model(SIMULATION_TIMESTEPS)
    data_2 = get_tracking_data(abm_2)
    save_tracking_data(data_2, SIMULATION_IO_DIRECTORY, 'copy2', verbose=False)

    for key in data_1.keys():
        assert data_1[key].equals(data_2[key])
