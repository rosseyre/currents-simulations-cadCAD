"""
CURRENTS Ecosystem Model
"""
__version__ = "0.1"

from radcad import Model

from system_parameters import parameters
from state_variables import initial_state
from state_update_blocks import state_update_blocks


# Instantiate a new Model
model = Model(
    params=parameters,
    initial_state=initial_state,
    state_update_blocks=state_update_blocks,
)
