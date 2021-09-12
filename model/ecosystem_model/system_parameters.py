"""
Definition of System Parameters, their types, and default values.

By using a dataclass to represent the System Parameters:
* We can use types for Python type hints
* Set default values
* Ensure that all System Parameters are initialized
"""

import numpy as np
from dataclasses import dataclass

from model.utils import default
from model.types import (
    List,
    Percentage
)


@dataclass
class Parameters:

    """System Parameters
    Each System Parameter is defined as:
    system parameter key: system parameter type = default system parameter value

    Because lists are mutable, we need to wrap each parameter list in the `default(...)` method.

    For default value assumptions, see the ASSUMPTIONS.md document.
    """


    initial_population: List[int] = default([10000])

    onboarding_coefficient: List[Percentage] = default([0.1]) # (%) adjust onboarding rate 
    
    client_competitor_price: List[float] = default([0.5]) # (ZAR/Mbps/Day) equivelent to AVG host service 
    avg_client_allocation: List[int] = default([10]) # (Mbps) 'Bandwidth' 
    client_registration_delay: List[int] = default([7]) # (Day)
    
    host_line_cost: List[Percentage] = default([0.5]) # (ZAR/Mbps/Day) ISP package
    avg_host_line: List[int] = default([1000]) # (Mbps) Backhaul capacity
    network_inefficiencies: List[Percentage] = default([0.25]) # (%) losses due to hardware inefficiencies, downtime, environemnt, etc. 
    host_setup_delay: List[int] = default([60]) # (Day)
    host_technical_difficulty: List[Percentage] = default([0.25]) # (%) threshold for host onboarding



# Initialize Parameters instance with default values
parameters = Parameters().__dict__
