"""
# Policy functions return an Input/Signal (Python dictionary) which is used by State Update functions to update the state.
"""

from model.types import Percentage



def p_client_adoption(params, substep, state_history, previous_state):
    
    return {"clients": clients}


def p_host_adoption(params, substep, state_history, previous_state):
    
    return {"hosts": hosts}


def p_demand(params, substep, state_history, previous_state):
    
    return {"demand": demand}


def p_price(params, substep, state_history, previous_state):
    
    return {"price": price}


def p_allocation(params, substep, state_history, previous_state):
    
    return {"allocation": allocation}