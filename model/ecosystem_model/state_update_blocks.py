"""
cadCAD model State Update Block structure, composed of Policy and State Update Functions
"""


import ecosystem_model.system_parameters
import ecosystem_model.policy_functions as policy
import ecosystem_model.state_update_functions as state
# from model.utils import update_from_signal


state_update_blocks = (

    {
        "description": """
            Default state-update block
        """,
        "policies": {
            "client_adoption": policy.p_client_adoption,
            "host_adoption": policy.p_host_adoption ,
            "indicated_demand": policy.p_indicated_demand,
            "network_allocation": policy.p_network_allocation,
            "network_penetration": policy.p_network_penetration,
            "avg_price": policy.p_price
        },
        "variables": {
            "clients": state.s_clients,
            "hosts": state.s_hosts,
            "potential_users": state.s_potential_users,
            "network_capacity": state.s_capacity,
            "network_demand": state.s_indicated_demand,
            "network_allocation": state.s_network_allocation,
            "network_penetration": state.s_network_penetration,
            "avg_price": state.s_price

        }
    }

)