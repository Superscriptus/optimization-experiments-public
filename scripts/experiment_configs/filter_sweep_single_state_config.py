from pathlib import Path

CONFIG = {
    0: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 42,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'random',  # algorithm to use for team allocation
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeats to run at each filter size
    },
    1: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 42,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'linear',  # algorithm to use for team allocation
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeats to run at each filter size
    },
    2: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 42,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'greedy',  # algorithm to use for team allocation
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeats to run at each filter size
    },
    3: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 42,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'grasp',  # algorithm to use for team allocation
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeats to run at each filter size
    },        
    4: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 42,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'reinforcement_learning',  # algorithm to use for team allocation
        'RL_N_REPEAT_SOLUTIONS': 1000,  # number of repeat team allocations to run at each filter size
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeat team allocations to run at each filter size
    },
    5: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 52,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'random',  # algorithm to use for team allocation
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeats to run at each filter size
    },
    6: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 52,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'linear',  # algorithm to use for team allocation
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeats to run at each filter size
    },
    7: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 52,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'greedy',  # algorithm to use for team allocation
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeats to run at each filter size
    },
    8: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 52,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'grasp',  # algorithm to use for team allocation
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeats to run at each filter size
    },        
    9: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 52,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'reinforcement_learning',  # algorithm to use for team allocation
        'RL_N_REPEAT_SOLUTIONS': 10,  # number of repeat team allocations to run at each filter size
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeat team allocations to run at each filter size
    },
    10: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 52,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'reinforcement_learning',  # algorithm to use for team allocation
        'RL_N_REPEAT_SOLUTIONS': 100,  # number of repeat team allocations to run at each filter size
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeat team allocations to run at each filter size
    },
    11: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 52,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'reinforcement_learning',  # algorithm to use for team allocation
        'RL_N_REPEAT_SOLUTIONS': 1000,  # number of repeat team allocations to run at each filter size
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeat team allocations to run at each filter size
    },
    12: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 5,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'random',  # algorithm to use for team allocation
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeats to run at each filter size
    },
    13: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 5,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'linear',  # algorithm to use for team allocation
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeats to run at each filter size
    },
    14: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 5,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'greedy',  # algorithm to use for team allocation
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeats to run at each filter size
    },
    15: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 5,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'grasp',  # algorithm to use for team allocation
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeats to run at each filter size
    },        
    16: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 5,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'reinforcement_learning',  # algorithm to use for team allocation
        'RL_N_REPEAT_SOLUTIONS': 10,  # number of repeat team allocations to run at each filter size
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeat team allocations to run at each filter size
    },
    17: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 5,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'reinforcement_learning',  # algorithm to use for team allocation
        'RL_N_REPEAT_SOLUTIONS': 100,  # number of repeat team allocations to run at each filter size
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeat team allocations to run at each filter size
    },
    18: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'STATE_ID': 5,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'reinforcement_learning',  # algorithm to use for team allocation
        'RL_N_REPEAT_SOLUTIONS': 1000,  # number of repeat team allocations to run at each filter size
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeat team allocations to run at each filter size
    }, 
    19: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_2',  # test dataset to use
        'STATE_ID': 5,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'random',  # algorithm to use for team allocation
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeats to run at each filter size
    },
    20: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_2',  # test dataset to use
        'STATE_ID': 5,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'linear',  # algorithm to use for team allocation
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeats to run at each filter size
    },
    21: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_2',  # test dataset to use
        'STATE_ID': 5,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'greedy',  # algorithm to use for team allocation
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeats to run at each filter size
    },
    22: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_2',  # test dataset to use
        'STATE_ID': 5,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'grasp',  # algorithm to use for team allocation
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeats to run at each filter size
    },        
    23: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_2',  # test dataset to use
        'STATE_ID': 5,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'reinforcement_learning',  # algorithm to use for team allocation
        'RL_N_REPEAT_SOLUTIONS': 10,  # number of repeat team allocations to run at each filter size
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeat team allocations to run at each filter size
    },
    24: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_2',  # test dataset to use
        'STATE_ID': 5,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'reinforcement_learning',  # algorithm to use for team allocation
        'RL_N_REPEAT_SOLUTIONS': 100,  # number of repeat team allocations to run at each filter size
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeat team allocations to run at each filter size
    },
    25: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_2',  # test dataset to use
        'STATE_ID': 5,  # state to use (states in all dataset are labelled with an integer ID)
        'NOTE': """
                    First trial experiment to check filter sweep is working as expected.
                """,
        'OPTIMISER': 'reinforcement_learning',  # algorithm to use for team allocation
        'RL_N_REPEAT_SOLUTIONS': 1000,  # number of repeat team allocations to run at each filter size
        'RUNNER': 'series',  # type of runner to use (series or parallel)
        # TODO: add config for optimiser and runner...
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_single_state',
        'N_REPEATS': 1,  # number of repeat team allocations to run at each filter size
    },
}
