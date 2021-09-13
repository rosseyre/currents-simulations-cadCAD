"""
# State Update Functions receive an Input/Signal (Python dictionary) from a policy function, and update the value of the state variable accordingly.
"""



def s_clients(params, substep, state_history, previous_state, policy_input):
    clients = policy_input["clients"] 
    return ("clients", clients)

def s_hosts(params, substep, state_history, previous_state, policy_input):
    hosts = policy_input["hosts"] 
    return ("hosts", hosts)

def s_potential_users(params, substep, state_history, previous_state, policy_input):

    
    potential_users = previous_state["potential_users"] - policy_input["clients"] - policy_input["hosts"] 
    if(potential_users < 0):
        potential_users = 1

    return ("potential_users", potential_users)

def s_network_capacity(params, substep, state_history, previous_state, policy_input):
    network_capacity = policy_input["network_capacity"] 
    return ("network_capacity", network_capacity)

def s_indicated_network_demand(params, substep, state_history, previous_state, policy_input):
    indicated_network_demand = policy_input["indicated_network_demand"] 
    return ("indicated_network_demand", indicated_network_demand)

def s_network_allocation(params, substep, state_history, previous_state, policy_input):
    network_allocation = policy_input["network_allocation"] 
    return ("network_allocation", network_allocation)

def s_network_penetration(params, substep, state_history, previous_state, policy_input):
    network_penetration = policy_input["network_penetration"] 
    return ("network_penetration", network_penetration)


def s_avg_price(params, substep, state_history, previous_state, policy_input):
    avg_price = policy_input["avg_price"] 
    return ("avg_price", avg_price)