# Dynamical-systems Models | CURRENTS

## Description

Dynamical-systems models for simulating and analysing the CURRENTS ecosystem, based on the open-source Python libraries radCAD / cadCAD

## Plot examples

#### Network adoption:
![alt text](https://github.com/rosseyre/currents-simulations/blob/main/img/network_adoption_1.png)

#### Daily revenue & profit:
![alt text](https://github.com/rosseyre/currents-simulations/blob/main/img/daily_yields.png)

#### AVG Price:
![alt text](https://github.com/rosseyre/currents-simulations/blob/main/img/price_plot_1.png)


## Differential model Specifications

![alt text](https://github.com/rosseyre/currents-simulations/blob/main/img/Currents-Diff-spec_1.png)

## Directory Structure

- data/: Datasets and API data sources
- docs/: Misc. documentation
- experiments/: Analysis notebooks and experiment workflow (e.g. configuration and execution)
- logs/: Experiment runtime log files
- model/: Model software architecture (structural and configuration modules)
- tests/: Unit and integration tests for model and notebooks

<i>Parts of this project, particularly the project structure and modular experiment workflow, is inspired by the open-source <a href="">Ethereum Economic Model</a> originally developed by CADLabs. </i>

## Environment Setup

1. Clone or download the Git repository
2. Setup your development environment using one of the options below:

### Option 1: Anaconda Development Environment

This option guides you through setting up a cross-platform development environment using Anaconda to install Python 3 and Jupyter.

1. Download [Anaconda](https://www.anaconda.com/products/individual)
2. Use Anaconda to install Python 3
3. Set up a virtual environment from within Anaconda
4. Install Jupyter Notebook within the virtual environment
5. Launch Jupyter Notebook and open the (environment_setup.ipynb) notebook in the root of the project repo
6. Follow and execute all notebook cells to install and check your Python dependencies

### Option 2: Custom Development Environment

This option guides you through how to set up a custom development environment using Python 3 and Jupyter.

Please note the following prerequisites before getting started:

Python: tested with versions 3.7, 3.8, 3.9

- NodeJS might be needed if using Plotly with Jupyter Lab (Plotly works out the box when using the Anaconda/Conda package manager with Jupyter Lab or Jupyter Notebook)
- First, set up a Python 3 virtualenv development environment (or use the equivalent Anaconda step):

##### Create a virtual environment using Python 3 venv module

```bash
python3 -m venv venv
```

##### Activate virtual environment

```bash
source venv/bin/activate
```

Make sure to activate the virtual environment before each of the following steps.

Secondly, install the Python 3 dependencies using Pip, from the requirements.txt file within your new virtual environment:

##### Install Python 3 dependencies inside virtual environment

```bash
pip install -r requirements.txt
```

To create a new Jupyter Kernel specifically for this environment, execute the following command:

```bash
python3 -m ipykernel install --user --name python-cadlabs-eth-model --display-name "Python (CURRENTS)"
```

You'll then be able to select the kernel with display name Python (CURRENTS) to use for your notebook from within Jupyter.

To start Jupyter Notebook or Lab (see notes about issues with using Plotly with Jupyter Lab):

```bash
jupyter notebook
```

##### Or:

```bash
jupyter lab
```

---

