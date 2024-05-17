from pathlib import Path
from . import meal_model
from sbmlutils.factory import ValidationOptions, FactoryResult
from sbmlutils.factory import create_model

import pandas as pd
import roadrunner

MEALMODEL_PATH = Path(__file__).parent

MODEL_BASE_PATH = MEALMODEL_PATH / "results"
MODEL_PATH = MODEL_BASE_PATH / "meal_model.xml"


def create_sbml_model(save_location: Path = MODEL_PATH) -> FactoryResult:
    """
    Create the SBML model and save it in the location specified
    Args:
        save_location: path where the file has to be saved

    Returns:
        FactoryResult

    """

    return create_model(
        filepath=save_location, model=meal_model.get_model(),
        validation_options=ValidationOptions(units_consistency=True, modeling_practice=False)
    )


def run_simulation(sbml_path: Path, start_time: int, end_time: int, steps_number: int) -> pd.DataFrame:
    """
    Run the simulation of the model.

    Args:
        sbml_path: path to the sbml file containing the model
        start_time: start time of the simulation
        end_time: end time of the simulation
        steps_number: number of steps between the start and end time


    Returns:
        dataframe containing the simulation results

    """

    r: roadrunner.RoadRunner = roadrunner.RoadRunner(str(sbml_path))
    _s = r.simulate(start=start_time, end=end_time, steps=steps_number)
    s_out = pd.DataFrame(_s, columns=_s.colnames)

    return s_out
