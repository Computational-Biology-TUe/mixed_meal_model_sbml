## Badges

(Customize these badges with your own links, and check https://shields.io/ or https://badgen.net/ to see which other badges are available.)

| fair-software.eu recommendations | |
| :-- | :--  |
| (1/5) code repository              | [![github repo badge](https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue)](https://github.com/Computational-Biology-TUe/mixed_meal_model_sbml) |
| (2/5) license                      | [![github license badge](https://img.shields.io/github/license/Computational-Biology-TUe/mixed_meal_model_sbml)](https://github.com/Computational-Biology-TUe/mixed_meal_model_sbml) |
| (3/5) community registry           | [![RSD](https://img.shields.io/badge/rsd-mixed_meal_model_sbml-00a3e3.svg)](https://research-software-directory.org/software/mixed-meal-model-sbml) |
| (4/5) citation                     | [![DOI](https://zenodo.org/badge/DOI/<replace-with-created-DOI>.svg)](https://doi.org/<replace-with-created-DOI>) |
| (5/5) checklist                    | [![workflow cii badge](https://bestpractices.coreinfrastructure.org/projects/8953/badge)](https://bestpractices.coreinfrastructure.org/projects/8953) |
| howfairis                          | [![fair-software badge](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B-yellow)](https://fair-software.eu) |
| **GitHub Actions**                 | &nbsp; |
| Build                              | [![build](https://github.com/Computational-Biology-TUe/mixed_meal_model_sbml/actions/workflows/build.yml/badge.svg)](https://github.com/Computational-Biology-TUe/mixed_meal_model_sbml/actions/workflows/build.yml) |
| Citation data consistency          | [![cffconvert](https://github.com/Computational-Biology-TUe/mixed_meal_model_sbml/actions/workflows/cffconvert.yml/badge.svg)](https://github.com/Computational-Biology-TUe/mixed_meal_model_sbml/actions/workflows/cffconvert.yml) |
| MarkDown link checker              | [![markdown-link-check](https://github.com/Computational-Biology-TUe/mixed_meal_model_sbml/actions/workflows/markdown-link-check.yml/badge.svg)](https://github.com/Computational-Biology-TUe/mixed_meal_model_sbml/actions/workflows/markdown-link-check.yml) |

# The mixed_meal_model_sbml

This is the codebase for generating SBML model of the Mixed Meal Model. 
The original model has been originally developed by S.D. O'Donovan[^1].

The Matlab implementation of the model can be found [here](https://github.com/Computational-Biology-TUe/Mixed_Meal_Model) 
and the Julia implementation can be found [here](https://github.com/max-de-rooij/MealModel.jl/edit/main/README.md)

The project setup is documented in [project_setup.md](project_setup.md). Feel free to remove this document (and/or the link to this document) if you don't need it.

## Installation

To install mixed_meal_model_sbml from GitHub repository, do:

```console
git clone git@github.com:Computational-Biology-TUe/mixed_meal_model_sbml.git
cd mixed_meal_model_sbml
python -m pip install .
```

## Using the mixed_meal_model_sbml package

### Generating the SBML model

In order to generate a new file containing the SBML model of the Mixed Meal Model, 
use the following:

```python
import mixed_meal_model_sbml

model_path = "my_path/meal_model.xml"

model = mixed_meal_model_sbml.create_sbml_model(model_path)
```

This will create a new .xml file containing the SBML definition of the model at the location specified.
If no path is specified, the model will be saved in  `/results/meal_model.xml`.

### Running a simulation

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

## Code structure

The definition of the model is contained in `meal_model.py`. This file contains the definitions
of the Compartments, Species, Parameters and Rules that constitute the model.

The measurement units are defined in `templates.py` and are used in the model definition.

The annotations used in the model are defined in `annotations.py`

## Contributing

If you want to contribute to the development of mixed_meal_model_sbml,
have a look at the [contribution guidelines](CONTRIBUTING.md).

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [NLeSC/python-template](https://github.com/NLeSC/python-template).

## References
[^1]: O’Donovan, S. D., Erdős, B., Jacobs, D. M., Wanders, A. J., Thomas, E. L., Bell, J. D., Rundle, M., Frost, G., Arts, I. C. W., Afman, L. A., & van Riel, N. A. W. (2022). Quantifying the contribution of triglycerides to metabolic resilience through the mixed meal model. IScience, 25(11), 105206. https://doi.org/10.1016/J.ISCI.2022.105206