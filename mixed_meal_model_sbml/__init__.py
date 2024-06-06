from pathlib import Path
import pandas as pd
import roadrunner
from sbmlutils.factory import FactoryResult
from sbmlutils.factory import ValidationOptions
from sbmlutils.factory import create_model
from . import meal_model

meal_model.Model.model_config["protected_namespaces"] = ()

MEALMODEL_PATH = Path(__file__).parent

MODEL_BASE_PATH = MEALMODEL_PATH / "results"
MODEL_PATH = MODEL_BASE_PATH / "meal_model.xml"

OUTPUT_PARAMETERS = [
    "glucose_plasma_flux",
    "hepatic_glucose_flux",
    "glucose_uptake",
    "[g_plasma]",
    "[I_PL]",
    "tg_plasma_flux",
    "hepatic_tg_flux",
    "[tg_plasma]",
    "[nefa_plasma]",
]


def create_sbml_model(save_location: Path = MODEL_PATH) -> FactoryResult:
    """Create the SBML model and save it in the location specified.

    Args:
        save_location: path where the file has to be saved

    Returns:
        FactoryResult

    """
    return create_model(
        filepath=save_location,
        model=meal_model.get_model(),
        validation_options=ValidationOptions(units_consistency=True, modeling_practice=False),
    )


def run_simulation(
    sbml_path: Path, start_time: int, end_time: int, steps_number: int, outputs: list[str] = OUTPUT_PARAMETERS
) -> pd.DataFrame:
    """Run the simulation of the model.

    Args:
        sbml_path: path to the sbml file containing the model
        start_time: start time of the simulation
        end_time: end time of the simulation
        steps_number: number of steps between the start and end time
        outputs: list of the variables to be returned by the model.
        It is a list containing the name of the variables as defined in the SBML model.


    Returns:
        dataframe containing the simulation results

    """
    r: roadrunner.RoadRunner = roadrunner.RoadRunner(str(sbml_path))

    _s = r.simulate(start=start_time, end=end_time, steps=steps_number, selections=outputs)
    s_out = pd.DataFrame(_s, columns=_s.colnames)

    return s_out
