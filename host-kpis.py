#!/usr/bin/env python
# coding: utf-8

# # Host KPI Systems Model (cadCAD) | CURRENTS Connect
# 
# ### Model introduction
# 
# Based on the host's individual parameters, the model simulates relevent network states and financial KPIs.
# 
# ### Assumptions
#  
# 
# ### Constraints / Scope
# 

# # 0. Dependencies

# In[1]:


# Standard libraries: https://docs.python.org/3/library/
import math
from numpy import random
import numpy as np

# Analysis and plotting modules
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from random import normalvariate

# cadCAD configuration modules
from cadCAD.configuration.utils import config_sim
from cadCAD.configuration import Experiment

# cadCAD simulation engine modules
from cadCAD.engine import ExecutionContext, Executor


# # 1. State Variables & System Parameters

# In[2]:


# Time horizon (Days)
timeHorizon = 365


# System states (python dictionaries):
initial_state = {
    'clients': 0,
    'host_revenue': 0,
    'demand': 0,
    'host_revenue': 0,
    'host_profit': 0,
    'host_expenses': 0,
    'cumulative_profit': 0

}


# System parameters (python lists):

system_params = {
    'price': [0.3],
    'host_line_cost': [0.06],
    'host_capacity': [2000],
    'potential_clients': [100], 
    'operating_expenses': [10],
    'avg_client_allocation': [10, 30, 10, 30],
    'platform_fee': [0.02],
    'client_acquisition_rate_coeff': [0.013, 0.013, 0.016, 0.016]
        
}


MONTE_CARLO_RUNS = 1

#flexible way to create unique seeds for each monte carlo run
seeds = [random.RandomState(i) for i in range(MONTE_CARLO_RUNS)] 


# # 2. Policy functions

# In[3]:


# Returns a dictionary
# Never updates a state directly. Rather, it returns an Input/Signal which is used by a State Update function to update the state



def p_client_acquisition(params, substep, state_history, previous_state):
    
    
    hostCapacity = params['host_capacity']
    clientAllocation = params['avg_client_allocation']
    
    maxClients = hostCapacity/clientAllocation
    
    if(maxClients > previous_state['clients']):
    
        # S-shaped growth representing client acquisition ('diffusion of innovation')
        
        x = previous_state['timestep']
        mp = timeHorizon/2 # midpoint of sigmoid
        #k = 0.015 # steepness of curve (default)
        k = params['client_acquisition_rate_coeff']
        height = params['potential_clients']

        clients = height / (1+ math.e**(-k*(x-mp))) 
        clients = int(clients)
        
    else:
        clients = maxClients
    
    return {'newClients': clients}


# calculate daily demand 
def p_demand(params, substep, state_history, previous_state):
    
    demand = previous_state['clients'] * params['avg_client_allocation']
    
    return {'demand': demand}



def p_revenue(params, substep, state_history, previous_state):
    
    revenue = previous_state['demand'] * params['price']
    
    return {'host_revenue': revenue}



def p_expenses(params, substep, state_history, previous_state):
    
    platformCommission = previous_state['host_revenue'] * params['platform_fee']
    
    expenses = (params['host_line_cost']*params['host_capacity']) + params['operating_expenses'] - platformCommission
    
    return {'host_expenses': expenses}



def p_profit(params, substep, state_history, previous_state):
    
    profit = previous_state['host_revenue'] - previous_state['host_expenses']
    
    return {'host_profit': profit}

def p_cumulative_profit(params, substep, state_history, previous_state):
    
    cumulativeProfit = previous_state['cumulative_profit'] + previous_state['host_profit']
    
    return {'cumulative_profit': cumulativeProfit}



# # 3. State Update Functions

# In[4]:


# Update number of clients based on s-curve
def s_clients(params, substep, state_history, previous_state, policy_input):
    
    x = policy_input['newClients'] 
    
    return ('clients', x)



# Update daily demand (i.e. bandwidth allocation)
def s_demand(params, substep, state_history, previous_state, policy_input):
    
    x = policy_input['demand']
    
    return ('demand', x)



# Update daily revenue
def s_revenue(params, substep, state_history, previous_state, policy_input): 
    
    x = policy_input['host_revenue']
    
    return ('host_revenue', x)



# Update daily expenses
def s_expenses(params, substep, state_history, previous_state, policy_input):  
    
    x = policy_input['host_expenses']
    
    return ('host_expenses', x)



# Update daily profit
def s_profit(params, substep, state_history, previous_state, policy_input):  
    
    x = policy_input['host_profit'];
    
    return ('host_profit', x)

# Update cumulative profit
def s_cumulative_profit(params, substep, state_history, previous_state, policy_input):  
    
    x = policy_input['cumulative_profit'];
    
    return ('cumulative_profit', x)





# # 4. Partial State Update Blocks

# In[5]:


partial_state_update_blocks = [
    {
        'policies': {
            'client_acquisition': p_client_acquisition,
            'demand': p_demand,
            'revenue': p_revenue,
            'expenses': p_expenses,
            'profit': p_profit,
            'cumulative_profit': p_cumulative_profit
        },
        'variables': {
            'active_clients': s_clients,
            'demand': s_demand,
            'revenue': s_revenue,
            'expenses': s_expenses,
            'profit': s_profit,
            'cumulative_profit': s_cumulative_profit
        }
    }
]


# # 5. Simulation Execution

# In[6]:


from cadCAD import configs
del configs[:] # Clear any prior configs


sim_config = config_sim({
    'N': 1,
    'T': range(timeHorizon),
    'M': system_params
})


experiment = Experiment()
experiment.append_configs(
    initial_state = initial_state,
    partial_state_update_blocks = partial_state_update_blocks,
    sim_configs = sim_config
)



exec_context = ExecutionContext()
run = Executor(exec_context=exec_context, configs=configs)

(system_events, tensor_field, sessions) = run.execute()


# # 6. Simulation Output Preparation

# ### Clean substeps

# In[7]:




# Convert system events dictionary into a pandas dataframe
# Get system events and attribute index
df = (pd.DataFrame(system_events)
      .assign(Days=lambda df: df.timestep)
      .query('timestep > 5')
     )

# Clean substeps
first_ind = (df.substep == 0) & (df.timestep == 0)
last_ind = df.substep == max(df.substep)
inds_to_drop = (first_ind | last_ind)
df = df.loc[inds_to_drop].drop(columns=['substep'])

# Attribute parameters to each row
df = df.assign(**configs[0].sim_config['M'])
for i, (_, n_df) in enumerate(df.groupby(['simulation', 'subset', 'run'])):
    df.loc[n_df.index] = n_df.assign(**configs[i].sim_config['M'])
    


# ### Check initial data

# In[8]:


simulation_result = pd.DataFrame(system_events)
simulation_result.tail(10)


# ### Convert data to JSON

# In[9]:


simulation_result


# In[10]:


# See pandas reference for different formatting: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_json.html

sim_json = simulation_result.to_json(orient='records', lines=True)

sim_json


# # 7. Plot data

# ### a) Client acquisition over time 
# 
# <p> 'subset' represents a simulation with a unique set of system parameters according to those defined in system_params.</p>

# In[11]:


fig_df = df

fig = px.line(
    fig_df,
    x='Days',
    y='clients',
    facet_row='subset',    
)

fig.show()


# In[12]:


#fig_df = df.query('avg_client_allocation == 10')
fig_df = df.query('client_acquisition_rate_coeff == 0.016')


fig = px.line(
    fig_df,
    x='Days',
    y=['host_revenue', 'demand'],
    height=500,
    animation_frame='avg_client_allocation'
)

fig.show()


# In[13]:


fig_df = df.query('avg_client_allocation == 10')

fig = px.line(
    fig_df,
    x='Days',
    y=['host_revenue', 'host_expenses', 'host_profit'],
    height=500,
    animation_frame='client_acquisition_rate_coeff'
)

fig.show()


# In[14]:


fig_df = df.query('client_acquisition_rate_coeff == 0.016')


fig = px.line(
    fig_df,
    x='timestep',
    y='cumulative_profit',
    height=500,
    animation_frame='avg_client_allocation'
)

fig.show()


# ## Get insights directly from System Events

# #### Given the subset, when does the host become profitable?

# In[15]:


for timestep in system_events:
    if(timestep['subset'] == 3):
        if(timestep['cumulative_profit'] > 0):
            print('For parameter subset', timestep['subset'], 'the host becomes profitable after:\n', timestep['timestep'], 'days.')
            break
        


# In[ ]:




