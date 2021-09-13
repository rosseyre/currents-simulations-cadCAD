"""
# Policy functions return an Input/Signal (Python dictionary) which is used by State Update functions to update the state.
"""

import typing
from ecosystem_model.types import (Percentage, Person)
import ecosystem_model.constants as constant

def p_client_adoption(params, substep, state_history, previous_state) -> typing.Dict[str, Person]:
    
    onboarding_coeff = params["onboarding_coefficient"]
    competitor_price = params["client_competitor_price"]
    registration_delay = params["client_registration_delay"]

    avg_price = previous_state["avg_price"]
    hosts = previous_state["hosts"]
    clients = previous_state["clients"]
    potential_users = previous_state["potential_users"]

    # WORD-OF-MOUTH
    # Calculate the probability that a contact via word-of-mouth has already adopted 
    probability_adopted = (clients + hosts) / potential_users

    #Calculate price desirability (a percentage value where: 0 = no desirability, 1 = high desirability)
    price_desirability = Percentage(0)
    if (competitor_price-avg_price > 0):
        price_desirability = (competitor_price-avg_price)/competitor_price

    #Calculate the number of new clients who registered
    clientsRegistering = (onboarding_coeff * potential_users * price_desirability * (1-probability_adopted)) / registration_delay
    clients += clientsRegistering

    return {"clients": clients}


def p_host_adoption(params, substep, state_history, previous_state) -> typing.Dict[str, Person]:
    
    onboarding_coeff = params["onboarding_coefficient"]
    setup_delay = params["host_setup_delay"]
    host_line_cost = params["host_line_cost"]
    avg_host_line = params["avg_host_line"]
    technical_difficulty = params["host_technical_difficulty"]
    MIN_min_expected_fulfillment = params["MIN_min_expected_fulfillment"]
    avg_client_allocation = params["avg_client_allocation"]

    avg_price = previous_state["avg_price"]
    hosts = previous_state["hosts"]
    clients = previous_state["clients"]
    potential_users = previous_state["potential_users"]
    network_penetration = previous_state["network_penetration"]

    # WORD-OF-MOUTH
    # Calculate the probability that a contact via word-of-mouth has already adopted 
    probability_adopted = (clients + hosts) / potential_users

    # Estimate the desire to become a host based on expected profit margins
    max_clients = avg_host_line / avg_client_allocation
    
    # Adjust fulfillment expectation based on actual network penetration
    host_expected_fulfillment = MIN_min_expected_fulfillment
    if (MIN_min_expected_fulfillment < network_penetration):
        host_expected_fulfillment = network_penetration

    expected_revenue = avg_price * max_clients * host_expected_fulfillment * avg_client_allocation
    operating_expenses = host_line_cost * avg_host_line

    profit = expected_revenue - operating_expenses
    if(profit > 0):
        expected_margin = profit / expected_revenue



    #Calculate the number of new hosts who registered
    hostsOnboarding = (onboarding_coeff * expected_margin * potential_users * (1-probability_adopted) * (1-technical_difficulty) ) / setup_delay
    hosts += hostsOnboarding


    return {"hosts": hosts}



#Calculate the total demand for connectivity (note: this is the indicated demand from registered clients, and not the actual allocated demand. For allocated demand, see 'network_allocation')
def p_indicated_demand(params, substep, state_history, previous_state) -> typing.Dict[str, Mbps]:
    
    competitor_price = params["client_competitor_price"]
    avg_client_allocation = params["avg_client_allocation"]

    avg_price = previous_state["avg_price"]
    clients = previous_state["clients"]

    price_attractiveness = competitor_price/avg_price
    if(price_attractiveness < 0):
        price_attractiveness = 0

    indicated_demand = clients * avg_client_allocation * price_attractiveness


    return {"indicated_demand": indicated_demand}



def p_network_allocation(params, substep, state_history, previous_state) -> typing.Dict[str, Mbps]:
    
    avg_client_allocation = params["avg_client_allocation"]

    clients = previous_state["clients"]
    network_penetration = previous_state["network_penetration"]

    price_attractiveness = competitor_price/avg_price
    if(price_attractiveness < 0):
        price_attractiveness = 0


    # To Do: what is the proper relationship between network penetration and access? Linear?
    access = network_penetration


    network_allocation = clients * avg_client_allocation * price_attractiveness * access

    return {"network_allocation": network_allocation}


def p_network_penetration(params, substep, state_history, previous_state) -> typing.Dict[str, Percentage]:
    
    hosts = previous_state["hosts"]
    potential_users = previous_state["potential_users"]

    max_clients_servicable_by_host = constant.max_clients_servicable_by_host 

    network_penetration = (hosts*max_clients_servicable_by_host) / potential_users

    return {"network_penetration": network_penetration}


# Price is determined by supply and demand
def p_price(params, substep, state_history, previous_state) -> typing.Dict[str, ZAR_per_Mbps]:

    avg_reserve_capacity = params["avg_reserve_capacity"]
    price_change_delay = params["price_change_delay"]
    
    currentPrice = previous_state["avg_price"]
    indicated_demand = previous_state["indicated_demand"]
    network_capacity = previous_state["network_capacity"]


    if (network_capacity != 0):
        supply_demand_ratio = indicated_demand / (network_capacity*(1-avg_reserve_capacity))
    else:
        supply_demand_ratio = 1


    desired_price = (currentPrice * supply_demand_ratio) 
    
    newPrice = (desired_price - currentPrice) / price_change_delay

    return {"price": newPrice}