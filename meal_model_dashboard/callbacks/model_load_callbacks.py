import base64
import math
import pandas as pd
import plotly.graph_objects as go
import roadrunner
from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import ctx
from libsbml import Model
from libsbml import readSBMLFromString
from plotly.subplots import make_subplots
import meal_model_dashboard.definitions.element_ids as ids
import meal_model_dashboard.definitions.layout_styles as styles
import mixed_meal_model_sbml as mm

model_rr: roadrunner.RoadRunner
model: Model


@callback(
    Output(ids.RUN_SIMULATION_BUTTON, "disabled"),
    Output(ids.PARAMETERS_CONTAINER, "hidden"),
    Output(ids.BODY_MASS_INPUT, "value"),
    Output(ids.FASTING_GLUCOSE_INPUT, "value"),
    Output(ids.FASTING_INSULIN_INPUT, "value"),
    Output(ids.FASTING_NEFA_INPUT, "value"),
    Output(ids.FASTING_TG_INPUT, "value"),
    Output(ids.MEAL_GLUCOSE_INPUT, "value"),
    Output(ids.MEAL_TG_INPUT, "value"),
    Output(ids.ERROR_MESSAGE, "children"),
    Output(ids.RESULTS_PLOTS, "style", allow_duplicate=True),
    Input(ids.UPLOAD_MODEL, "contents"),
    Input(ids.CREATE_MODEL_BUTTON, "n_clicks"),
    prevent_initial_call=True,
)
def load_sbml(content, btn_click):
    """Callback for file loading."""
    global model_rr
    global model
    run_btn_disabled = hidden_params = True
    bw = fasting_glucose = fasting_insulin = fasting_nefa = fasting_tg = mg = mtg = ""
    model_raw = None
    msg = ""

    trigger = ctx.triggered_id

    if trigger == ids.CREATE_MODEL_BUTTON:
        model_raw = mm.create_sbml_model().model.get_sbml()

    elif trigger == ids.UPLOAD_MODEL:
        content_type, content_string = content.split(",")

        if content_type == "data:text/xml;base64":
            model_raw = base64.b64decode(content_string).decode("utf-8")
        else:
            msg = "Wrong file type"

    try:
        model_rr = roadrunner.RoadRunner(model_raw)
        model = readSBMLFromString(model_raw).getModel()

        bw = model_rr["BW"]
        fasting_glucose = model_rr["fasting_glucose"]
        fasting_insulin = model_rr["fasting_insulin"]
        fasting_nefa = model_rr["fasting_NEFA"]
        fasting_tg = model_rr["fasting_TG"]
        mg = model_rr["mG"]
        mtg = model_rr["mTG"]

        run_btn_disabled = False
        hidden_params = False

    except Exception:
        msg = "Wrong model loaded"
        print(msg)

    return (
        run_btn_disabled,
        hidden_params,
        bw,
        fasting_glucose,
        fasting_insulin,
        fasting_nefa,
        fasting_tg,
        mg,
        mtg,
        msg,
        styles.EMPTY_ELEMENT,
    )


@callback(
    Output(ids.RESULTS_PLOTS, "figure"),
    Output(ids.RESULTS_PLOTS, "style", allow_duplicate=True),
    Input(ids.RUN_SIMULATION_BUTTON, "n_clicks"),
    State(ids.BODY_MASS_INPUT, "value"),
    State(ids.FASTING_GLUCOSE_INPUT, "value"),
    State(ids.FASTING_INSULIN_INPUT, "value"),
    State(ids.FASTING_NEFA_INPUT, "value"),
    State(ids.FASTING_TG_INPUT, "value"),
    State(ids.MEAL_GLUCOSE_INPUT, "value"),
    State(ids.MEAL_TG_INPUT, "value"),
    State(ids.START_TIME_INPUT, "value"),
    State(ids.STOP_TIME_INPUT, "value"),
    State(ids.STEPS_TIME_INPUT, "value"),
    prevent_initial_call=True,
)
def run_simulation(
    _,
    body_mass,
    fasting_glucose,
    fasting_insulin,
    fasting_nefa,
    fasting_tg,
    meal_glucose,
    meal_tg,
    start_time,
    stop_time,
    steps,
):
    """Run the simulation using the set parameters."""
    global model_rr

    model_rr["BW"] = body_mass
    model_rr["fasting_glucose"] = fasting_glucose
    model_rr["fasting_insulin"] = fasting_insulin
    model_rr["fasting_NEFA"] = fasting_nefa
    model_rr["fasting_TG"] = fasting_tg
    model_rr["mG"] = meal_glucose
    model_rr["mTG"] = meal_tg

    _s = model_rr.simulate(start=start_time, end=stop_time, steps=steps, selections=mm.OUTPUT_PARAMETERS)

    df = pd.DataFrame(_s, columns=_s.colnames)

    fig = plot_results(df, model)

    return fig, styles.GRAPH


def plot_results(df: pd.DataFrame, model_sbml: Model) -> go.Figure:
    """Plot the results of the simulation."""
    columns_n = 3
    rows_n = df.shape[1] // columns_n
    model_outputs = list(df.columns)

    fig = make_subplots(rows=rows_n, cols=3, subplot_titles=model_outputs)

    for n, output in enumerate(model_outputs, start=1):
        output_clean = output.replace("[", "").replace("]", "")

        param = model_sbml.parameters.getElementBySId(output_clean)
        extra = ""
        if not param:
            # species have to be reported as concentration
            param = model_sbml.species.getElementBySId(output_clean)
            extra = "/liter"

        try:
            unit = model_sbml.getUnitDefinition(param.getUnits()).name
            unit = f"{unit}{extra}"

        except AttributeError:
            print("None found")
            unit = ""

        row = math.ceil(n / columns_n)
        col = n - (row * columns_n) + columns_n
        fig.add_trace(go.Scatter(y=df[output]), row=row, col=col)

        fig.update_xaxes(title_text="time [min]", row=row, col=col)
        fig.update_yaxes(title_text=unit, row=row, col=col)
        fig.layout.annotations[n - 1].update(text=param.name)

    fig.update_layout(height=1500, width=1500, title_text="Simulation output", showlegend=False)

    return fig
