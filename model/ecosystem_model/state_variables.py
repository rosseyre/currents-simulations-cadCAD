from dataclasses import dataclass

import model.ecosystem_model.system_parameters as parameters
from model.types import (
    Percentage
)



timeHorizon = int(365) # (Days) 


@dataclass
class StateVariables:

    """State Variables
    Each State Variable is defined as:
    state variable key: state variable type = default state variable value
    """

    clients: int = 1
    hosts: int = 1
    potential_users: int = parameters["initial_population"][0]

    avg_price: float = 5 # (ZAR/Mbps/Day) The price hosts set for connectivity

    network_capacity: int = hosts * parameters["avg_host_line"][0] # (Mbps) Total host capacity
    network_demand: int = clients * parameters["avg_client_allocation"][0] # (Mbps) Estimated total demand for connectivity
    network_allocation: int = 0 # (Mbps) Actual allocated demand
    network_penetration: Percentage = 0 # (%) Population servicable by hosts (a function of network coverage)
    



# Initialize State Variables instance with default values
initial_state = StateVariables().__dict__