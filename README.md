## Badges

(Customize these badges with your own links, and check https://shields.io/ or https://badgen.net/ to see which other badges are available.)

| fair-software.eu recommendations | |
| :-- | :--  |
| (1/5) code repository              | [![github repo badge](https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue)](https://github.com/Computational-Biology-TUe/mixed_meal_model_sbml) |
| (2/5) license                      | [![github license badge](https://img.shields.io/github/license/Computational-Biology-TUe/mixed_meal_model_sbml)](https://github.com/Computational-Biology-TUe/mixed_meal_model_sbml) |
| (3/5) community registry           | [![RSD](https://img.shields.io/badge/rsd-mixed_meal_model_sbml-00a3e3.svg)](https://research-software-directory.org/software/mixed-meal-model-sbml) |
| (4/5) citation                     | [![DOI](https://zenodo.org/badge/781502181.svg)](https://zenodo.org/doi/10.5281/zenodo.11210057)
| (5/5) checklist                    | [![workflow cii badge](https://bestpractices.coreinfrastructure.org/projects/8953/badge)](https://bestpractices.coreinfrastructure.org/projects/8953) |
| howfairis                          | [![fair-software badge](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B-yellow)](https://fair-software.eu) |
| **GitHub Actions**                 | &nbsp; |
| Build                              | [![build](https://github.com/Computational-Biology-TUe/mixed_meal_model_sbml/actions/workflows/build.yml/badge.svg)](https://github.com/Computational-Biology-TUe/mixed_meal_model_sbml/actions/workflows/build.yml) |
| Citation data consistency          | [![cffconvert](https://github.com/Computational-Biology-TUe/mixed_meal_model_sbml/actions/workflows/cffconvert.yml/badge.svg)](https://github.com/Computational-Biology-TUe/mixed_meal_model_sbml/actions/workflows/cffconvert.yml) |
| MarkDown link checker              | [![markdown-link-check](https://github.com/Computational-Biology-TUe/mixed_meal_model_sbml/actions/workflows/markdown-link-check.yml/badge.svg)](https://github.com/Computational-Biology-TUe/mixed_meal_model_sbml/actions/workflows/markdown-link-check.yml) |

# The mixed_meal_model_sbml

This is the codebase for generating SBML model of the Mixed Meal Model, running simulations of the 
generated SBML model. The code include also a dashboard to set the simulation parameters
and visualizing the results.
The most recent version of the SBML model can be found [here](./mixed_meal_model_sbml/results/meal_model.xml).

It is possible to easily visualizing the model by using the [SBML4Human](https://sbml4humans.de/) online platform.

The original model has been originally developed by S.D. O'Donovan[^1].

The Matlab implementation of the model can be found [here](https://github.com/Computational-Biology-TUe/Mixed_Meal_Model) 
and the Julia implementation can be found [here](https://github.com/max-de-rooij/MealModel.jl/edit/main/README.md)

The project setup is documented in [project_setup.md](project_setup.md). 

## Installation

To install mixed_meal_model_sbml from GitHub repository, do:

```commandline
git clone git@github.com:Computational-Biology-TUe/mixed_meal_model_sbml.git
cd mixed_meal_model_sbml
python -m pip install .
```

## Using the mixed_meal_model_sbml package

### Command line interface (CLI)

The package comes with a CLI for running the principal functionalities. 
It is possible to list the available commands by running 
```commandline
mixed-model --help
```

#### Generate a new SBML file
 
The `create-model` command can be used to generate a file. 
The path where the file has to be saved has to be specified using the `--path` option. For example:

```commandline
mixed-model create-model --path /my_path/model.xml
```

The SBML model will be generated and saved in the specified path.


#### Run a simulation

The `run-simulation` command can be used run a simulation and save the results as a csv file, 
using the following options:  
-  `--file-path`: path where the SBML model can be found.
-  `--start-time`: initial simulation time.
-  `--end-time`: end simulation time.
-  `--steps`: number of steps between the start and end time.
-  `--save-path`: path where to save the results as csv file.

For example:
```commandline
meal-model run-simulation --file-path .\mixed_meal_model_sbml\results\meal_model.xml --start-time 0 --end-time 500 --steps 500 --save-path .\mixed_meal_model_sbml\results\meal_model.csv
```
### Using the code base

#### Generating the SBML model

In order to generate a new file containing the SBML model of the Mixed Meal Model 
using the python code, use the following:

```python
import mixed_meal_model_sbml

model_path = "my_path/meal_model.xml"

model = mixed_meal_model_sbml.create_sbml_model(model_path)
```

This will create a new .xml file containing the SBML definition of the model at the location specified.
If no path is specified, the model will be saved in  `/results/meal_model.xml`.

#### Running a simulation

The package makes use of [roadrunner](https://github.com/sys-bio/roadrunner) to run the model simulations.
It is possible to run a simulation using the default parameters as shown here:

```python
import mixed_meal_model_sbml

model_path = "my_path/meal_model.xml"

results = mixed_meal_model_sbml.run_simulation(sbml_path=model_path,
                                               start_time=0,
                                               end_time=500,
                                               steps_number=500)
```

This code will run a simulation of the model from time 0 to time 500 using 500 steps. 
The results are returned as a Pandas DataFrame containing the values of the species 
calculated at each time step.

#### Code structure

The definition of the model is contained in `meal_model.py`. This file contains the definitions
of the Compartments, Species, Parameters and Rules that constitute the model.

The measurement units are defined in `templates.py` and are used in the model definition.

The annotations used in the model are defined in `annotations.py`

## Dashboard

The dashboard is a [Dash](https://dash.plotly.com/) based GUI that can be used to upload the model, modify the parameters and run the simulations.

It is possible to easily run the dashboard using the CLI:

```commandline
meal-model run-dashboard
```

A URL, typically http://127.0.0.1:8050/, will be printed, where the dashboard can be accessed.

It is also possible to run the dashboard by running the following command from the `mixed_meal_model_dashboard` folder:

```commandline
python main.py
```

And following the printed URL.



## Contributing

If you want to contribute to the development of mixed_meal_model_sbml,
have a look at the [contribution guidelines](CONTRIBUTING.md).


## References
[^1]: O’Donovan, S. D., Erdős, B., Jacobs, D. M., Wanders, A. J., Thomas, E. L., Bell, J. D., Rundle, M., Frost, G., Arts, I. C. W., Afman, L. A., & van Riel, N. A. W. (2022). Quantifying the contribution of triglycerides to metabolic resilience through the mixed meal model. IScience, 25(11), 105206. https://doi.org/10.1016/J.ISCI.2022.105206