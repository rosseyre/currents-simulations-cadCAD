"""
# Time Domain Analysis

Executes a time-domain simulation over a period of 1 year
"""

import copy

from experiments.default_experiment import experiment


# Make a copy of the default experiment to avoid mutation
experiment = copy.deepcopy(experiment)

TIMESTEPS = 365 # (Days)


"""
parameter_overrides = {
    "name": [newValue],
    "name2": [newValue2],
}
"""


# Override default experiment Simulation and System Parameters related to timing
experiment.simulations[0].timesteps = TIMESTEPS


# Override default experiment System Parameters
# experiment.simulations[0].model.params.update(parameter_overrides)