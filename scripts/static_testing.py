"""
Script to run 'static testing' experiments.

Here we run repeated team allocations for the same workforce state s and project p. We use the
same set of (w,p) pairs to test each algorithm.

The SuperScript ABM is used to create set of (w,p).

Note: random seeding is not enough to ensure reproducibility on different systems.
"""
import os
import pickle
import time
import shutil
from pathlib import Path
from superscript_model.model import SuperScriptModel
from superscript_model.optimisation_decoupled import StateSpaceRepresentation


# Set global config params for all ABMs
simulation_timesteps = 100
simulation_io_directory = Path('../test_data')
worker_count = 100
department_count = 10
projects_per_timestep = 2
departmental_workload = 0.1
organisation_strategy = 'Random'  # 'Basin'
data_collection = True
save_projects = True
load_projects = False
random_seed = 42

if __name__ == '__main__':
    print("G")

if False:



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
        data = {
            'model_variables': model.datacollector.get_model_vars_dataframe(),
            'project_table': model.datacollector.get_table_dataframe('Projects'),
            'agent_variables': model.datacollector.get_agent_vars_dataframe()
        }
        return data


    def create_and_run_model():

        start_time = time.time()
        abm = SuperScriptModel(
            worker_count=worker_count,
            department_count=department_count,
            new_projects_per_timestep=projects_per_timestep,
            organisation_strategy=organisation_strategy,
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

        os.makedirs(simulation_io_directory, exist_ok=False)

        if load_projects:
            shutil.copyfile(
                Path('training_data/example_project_file.pickle'),
                simulation_io_directory / 'project_file.pickle'
            )

        abm_1, data_1 = create_and_run_model()
        save_tracking_data(data_1, simulation_io_directory, 'base')

        # Here we create a model with the same random seed and config, and check that the outputs are the same:
        abm_2, data_2 = create_and_run_model()
        save_tracking_data(data_2, simulation_io_directory, 'seed')

        for key in data_1.keys():
            assert data_1[key].equals(data_2[key])

        # Now we copy the ABM from a completed simulation and restart it from time=0, using the same projects:
        abm_1 = SuperScriptModel.copy_existing_abm(
            abm_1,
            mode='restart',
            load_projects=True,
            save_projects=False,
            io_dir=simulation_io_directory
        )
        abm_1.run_model(simulation_timesteps)
        data_1 = get_tracking_data(abm_1)
        save_tracking_data(data_1, simulation_io_directory, 'copy1', verbose=False)

        abm_2 = SuperScriptModel.copy_existing_abm(
            abm_2,
            mode='restart',
            load_projects=True,
            save_projects=False,
            io_dir=simulation_io_directory
        )
        abm_2.run_model(simulation_timesteps)
        data_2 = get_tracking_data(abm_2)
        save_tracking_data(data_2, simulation_io_directory, 'copy2', verbose=False)

        for key in data_1.keys():
            assert data_1[key].equals(data_2[key])
