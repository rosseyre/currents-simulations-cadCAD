"""
cadCAD model State Update Block structure, composed of Policy and State Update Functions
"""


import model.ecosystem_model.system_parameters

_state_update_blocks = (

    {
        "description": """
            Default state-update block
        """,
        "policies": {
            "client_adoption": p_client_acquisition,
            "host_adoption": p_host_acquisition,
            "demand": p_demand,
            "price": p_price,
            "demand": p_demand,
        "variables": {
            "clients": s_clients,
            "hosts": s_hosts,
            "potential_users": s_potential_users,
            "network_capacity": s_capacity,
            "network_demand": s_demand,
            "network_allocation": s_allocation,
            "avg_price": s_price
        }
    }

)