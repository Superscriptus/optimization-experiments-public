from pathlib import Path

CONFIG = {
    0: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'NOTE': """
                    Filter sweep with as default algo parameters (note GRASP not performing well).
                    Using first_n filter.
                """,
        'OPTIMISERS': {
            #'random': {'RUNNER': 'series'},
            #'linear': {'RUNNER': 'series'},
            #'greedy': {'RUNNER': 'series'},
            #'grasp': {'RUNNER': 'series'},
            'rld2_10': {
                'RUNNER': 'series',
                'N_REPEAT_SOLUTIONS': 10
            },
            'rld2_100': {
                'RUNNER': 'series',
                'N_REPEAT_SOLUTIONS': 100
            },
            'rld2_1000': {
                'RUNNER': 'series',
                'N_REPEAT_SOLUTIONS': 1000
            },
        },  # algorithms and configs to use
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_multi_state',
        'N_REPEATS': 1,  # number of repeats to run for each filter size, algo and state
    },
    1: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'first_n',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'NOTE': """
                Filter sweep with default algo parameters (note GRASP not performing well).
                Parallel runner for RLD2 > 10.
                Using first_n filter.
            """,
        'OPTIMISERS': {
            'random': {'RUNNER': 'series'},
            'linear': {'RUNNER': 'series'},
            'greedy': {'RUNNER': 'series'},
            'grasp': {'RUNNER': 'series'},
            'rld2_10': {
                'RUNNER': 'series',
                'N_REPEAT_SOLUTIONS': 10
            },
            'rld2_100': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 10
            },
            'rld2_1000': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 100
            },
        },  # algorithms and configs to use
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_multi_state',
        'N_REPEATS': 1,  # number of repeats to run for each filter size, algo and state
    },
    2: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'ml_filter',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'NOTE': """
                Filter sweep with default algo parameters (note GRASP not performing well).
                Parallel runner for RLD2 > 10.
                Using ml filter.
            """,
        'OPTIMISERS': {
            # 'random': {'RUNNER': 'series'},
            # 'linear': {'RUNNER': 'series'},
            # 'greedy': {'RUNNER': 'series'},
            # 'grasp': {'RUNNER': 'series'},
            'rld2_1000': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 100
            },
            'rld2_10': {
                'RUNNER': 'series',
                'N_REPEAT_SOLUTIONS': 10
            },
            'rld2_100': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 10
            },
        },  # algorithms and configs to use
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_multi_state',
        'N_REPEATS': 1,  # number of repeats to run for each filter size, algo and state
    },
    3: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'random',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'NOTE': """
                Filter sweep with default algo parameters (note GRASP not performing well).
                Parallel runner for RLD2 > 10.
                Using randomfilter.
            """,
        'OPTIMISERS': {
            'random': {'RUNNER': 'series'},
            'linear': {'RUNNER': 'series'},
            'greedy': {'RUNNER': 'series'},
            'rld2_1000': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 100
            },
             'grasp': {'RUNNER': 'series'},
            'rld2_10': {
                'RUNNER': 'series',
                'N_REPEAT_SOLUTIONS': 10
            },
            'rld2_100': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 10
            },
        },  # algorithms and configs to use
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_multi_state',
        'N_REPEATS': 1,  # number of repeats to run for each filter size, algo and state
    },
    4: {
        'FILTER_SIZES': [10, 50, 100],
        'FILTER_TYPE': 'ml_filter',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'NOTE': """
                Redcued filter sweep with RLD2 only, using RLD1 in stochastic mode.
                Parallel runner for RLD2 > 10.
                Using ml filter.
            """,
        'OPTIMISERS': {
            # 'random': {'RUNNER': 'series'},
            # 'linear': {'RUNNER': 'series'},
            # 'greedy': {'RUNNER': 'series'},
            # 'grasp': {'RUNNER': 'series'},
            'rld2_10_rld1_10': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 10
            },
            'rld2_1_rld1_100': {
                'RUNNER': 'series',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 100
            },
            'rld2_1_rld1_1': {
                'RUNNER': 'series',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 1
            },
            'rld2_1_rld1_10': {
                'RUNNER': 'series',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 1
            },
            'rld2_10_rld1_100': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 100
            },
            'rld2_100_rld1_10': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 10,
                'RLD1_REPEATS': 10
            },
        },  # algorithms and configs to use
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_multi_state',
        'N_REPEATS': 1,  # number of repeats to run for each filter size, algo and state
    },
    5: {
        'FILTER_SIZES': [10],
        'FILTER_TYPE': 'ml_filter',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'NOTE': """
                Single filter size to test long stochasitc runs w/ RLD2 and RLD1.
                Using ml filter.
            """,
        'OPTIMISERS': {
            # 'rld2_1000_rld1_10': {
            #     'RUNNER': 'parallel',
            #     'N_REPEAT_SOLUTIONS': 100,
            #     'RLD1_REPEATS': 10
            # },
            'rld2_1000_rld1_100': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 100,
                'RLD1_REPEATS': 100
            }
        },  # algorithms and configs to use
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_multi_state',
        'N_REPEATS': 1,  # number of repeats to run for each filter size, algo and state
    },
    6: {
        'FILTER_SIZES': [100],
        'FILTER_TYPE': 'ml_filter',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'NOTE': """
                Single filter size to test long stochasitc runs w/ RLD2 and RLD1.
                Using ml filter.
            """,
        'OPTIMISERS': {
            # 'rld2_1000_rld1_10': {
            #     'RUNNER': 'parallel',
            #     'N_REPEAT_SOLUTIONS': 100,
            #     'RLD1_REPEATS': 10
            # },
            'rld2_1000_rld1_100': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 100,
                'RLD1_REPEATS': 100
            }
        },  # algorithms and configs to use
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_multi_state',
        'N_REPEATS': 1,  # number of repeats to run for each filter size, algo and state
    },
    7: {
        'FILTER_SIZES': [10, 50, 100],
        'FILTER_TYPE': 'ml_filter',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'NOTE': """
                Quick test of new RLD2(v3.106_4) and RLD1(v4.645_2)
                Using ml filter.
            """,
        'OPTIMISERS': {
            'rld2_v3': {
                'RUNNER': 'series',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 1
            },
            'rld2_v3_10': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 1
            },
        },  # algorithms and configs to use
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_multi_state',
        'N_REPEATS': 1,  # number of repeats to run for each filter size, algo and state
    },
    8: {
        'FILTER_SIZES': [10, 50, 100],
        'FILTER_TYPE': 'ml_filter',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'NOTE': """
                More detailed test of new RLD2(v3.106_4) and RLD1(v4.645_2)
                Using ml filter.
            """,
        'OPTIMISERS': {
            'rld2_v3': {
                'RUNNER': 'series',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 1
            },
            'rld2_v3_10': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 1
            },
            'rld2_v3_100': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 10,
                'RLD1_REPEATS': 1
            },
            'rld2_v3_100_rld1_10': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 10,
                'RLD1_REPEATS': 10
            },
            'rld2_v3_10_rld1_10': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 10
            },
        },  # algorithms and configs to use
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_multi_state',
        'N_REPEATS': 1,  # number of repeats to run for each filter size, algo and state
    },
    9: {
        'FILTER_SIZES': [10, 50, 100],
        'FILTER_TYPE': 'random',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'NOTE': """
                More detailed test of new RLD2(v3.106_4) and RLD1(v4.645_2)
                Using random filter.
            """,
        'OPTIMISERS': {
            'rld2_v3_100': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 10,
                'RLD1_REPEATS': 1
            },
            'rld2_v3_100_rld1_10': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 10,
                'RLD1_REPEATS': 10
            },
            'rld2_v3_10_rld1_10': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 10
            },
        },  # algorithms and configs to use
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_multi_state',
        'N_REPEATS': 1,  # number of repeats to run for each filter size, algo and state
    },
    10: {
        'FILTER_SIZES': [10, 50, 100],
        'FILTER_TYPE': 'random',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'NOTE': """
                BUG! - constraint was not called. 
                Rerunning everything with new fixed constraints (no negative availability).
                Using random filter.
            """,
        'OPTIMISERS': {
            'random': {'RUNNER': 'series'},
            'linear': {'RUNNER': 'series'},
            'greedy': {'RUNNER': 'series'},
            'rld2_v3': {
                'RUNNER': 'series',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 1
            },
            'grasp': {'RUNNER': 'series'},
            'rld2_v3_10': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 1
            },
            'rld2_v3_100': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 10,
                'RLD1_REPEATS': 1
            },
            'rld2_v3_100_rld1_10': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 10,
                'RLD1_REPEATS': 10
            },
            'rld2_v3_10000_rld1_10': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 10
            },
        },  # algorithms and configs to use
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_multi_state',
        'N_REPEATS': 1,  # number of repeats to run for each filter size, algo and state
    },
    11: {
        'FILTER_SIZES': [10, 50, 100],
        'FILTER_TYPE': 'ml_filter',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'NOTE': """
                BUG! - constraint was not called. 
                Rerunning everything with new fixed constraints (no negative availability).
                Using ml filter.
            """,
        'OPTIMISERS': {
            'random': {'RUNNER': 'series'},
            'linear': {'RUNNER': 'series'},
            'greedy': {'RUNNER': 'series'},
            'rld2_v3': {
                'RUNNER': 'series',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 1
            },
             'grasp': {'RUNNER': 'series'},
            'rld2_v3_10': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 1
            },
            'rld2_v3_100': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 10,
                'RLD1_REPEATS': 1
            },
            'rld2_v3_100_rld1_10': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 10,
                'RLD1_REPEATS': 10
            },
            'rld2_v3_10000_rld1_10': {
                'RUNNER': 'parallel',
                'N_REPEAT_SOLUTIONS': 1,
                'RLD1_REPEATS': 10
            },
        },  # algorithms and configs to use
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_multi_state',
        'N_REPEATS': 1,  # number of repeats to run for each filter size, algo and state
    },
    12: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'random',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'NOTE': """
                Rerunning everything with new fixed constraints (no negative availability).
                Using random filter.
            """,
        'OPTIMISERS': {
            'random': {'RUNNER': 'series'},
            'linear': {'RUNNER': 'series'},
            'greedy': {'RUNNER': 'series'},
            'grasp': {'RUNNER': 'series'},
        },  # algorithms and configs to use
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_multi_state',
        'N_REPEATS': 1,  # number of repeats to run for each filter size, algo and state
    },
    13: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'ml_filter',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'NOTE': """
                Rerunning everything with new fixed constraints (no negative availability).
                Using ml filter.
            """,
        'OPTIMISERS': {
            'random': {'RUNNER': 'series'},
            'linear': {'RUNNER': 'series'},
            'greedy': {'RUNNER': 'series'},
            'grasp': {'RUNNER': 'series'}
        },  # algorithms and configs to use
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_multi_state',
        'N_REPEATS': 1,  # number of repeats to run for each filter size, algo and state
    },
    14: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'ml_filter',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'validation_dataset',  # dataset to use
        'NOTE': """
                Rerunning everything on new validation dataset with newest model versions (2/07/25).
                Using ml filter.
            """,
        'OPTIMISERS': {
            'random': {'RUNNER': 'series'},
            'linear': {'RUNNER': 'series'},
            'greedy': {'RUNNER': 'series'},
            'grasp': {'RUNNER': 'series'},
            'rld2_100_10': {
                'RUNNER': 'parallel',
                'rl_config_dict': {
                    'trained_model': 'RLD2-v3.106-nonlinear_2',
                    'hyperparameters': 'RLD2-v3.106-nonlinear',
                    'deterministic': False,
                    'num_repeats': 10,
                    'rld1_deterministic': False,
                    'rld1_num_repeats': 10,
                    'timeout': 1
                }
            }
        },  # algorithms and configs to use
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_multi_state',
        'N_REPEATS': 1,  # number of repeats to run for each filter size, algo and state
    },
    15: {
        'FILTER_SIZES': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'FILTER_TYPE': 'random',  # overrides ABM config filters
        'ABM_CONFIG_FILE': 'stage_1_config.yaml',  # used to override all other configs
        'DATASET': Path('test_data') / 'dataset_1',  # test dataset to use
        'DATASET': Path('test_data') / 'validation_dataset',  # dataset to use
        'NOTE': """
                Rerunning everything on new validation dataset with newest model versions (2/07/25).
                Using random.
            """,
        'OPTIMISERS': {
            'random': {'RUNNER': 'series'},
            'linear': {'RUNNER': 'series'},
            'greedy': {'RUNNER': 'series'},
            'grasp': {'RUNNER': 'series'},
            'rld2_100_10': {
                'RUNNER': 'parallel',
                'rl_config_dict': {
                    'trained_model': 'RLD2-v3.106-nonlinear_2',
                    'hyperparameters': 'RLD2-v3.106-nonlinear',
                    'deterministic': False,
                    'num_repeats': 10,
                    'rld1_deterministic': False,
                    'rld1_num_repeats': 10,
                    'timeout': 1
                }
            }
        },  # algorithms and configs to use
        'SAVE_TO': Path('stage_1_results') / 'filter_sweep_multi_state',
        'N_REPEATS': 1,  # number of repeats to run for each filter size, algo and state
    },
}
