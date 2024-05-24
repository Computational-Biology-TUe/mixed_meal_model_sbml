import base64
import roadrunner
from dash import Input
from dash import Output
from dash import State
from dash import callback
import meal_model_dashboard.definitions.element_ids as ids
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

model_rr: roadrunner.RoadRunner


@callback(
    Output(ids.RUN_SIMULATION_BUTTON, 'disabled'),
    Input(ids.UPLOAD_MODEL, 'contents'),
    prevent_initial_call=True,
)
def load_sbml(content):
    """Callback for file loading."""
    global model_rr
    run_btn_disabled = True

    content_type, content_string = content.split(',')

    if content_type == 'data:text/xml;base64':
        model = base64.b64decode(content_string).decode("utf-8")
        model_rr = roadrunner.RoadRunner(model)
        run_btn_disabled = False

    return run_btn_disabled


@callback(
    Output(ids.BODY_MASS_INPUT, "value"),
    Output(ids.FASTING_GLUCOSE_INPUT, "value"),
    Output(ids.FASTING_INSULIN_INPUT, "value"),
    Output(ids.FASTING_NEFA_INPUT, "value"),
    Output(ids.FASTING_TG_INPUT, "value"),
    Output(ids.MEAL_GLUCOSE_INPUT, "value"),
    Output(ids.MEAL_TG_INPUT, "value"),
    Input(ids.RUN_SIMULATION_BUTTON, 'disabled'),
    prevent_initial_call=True,
)
def populate_params(_):
    """Callback fo populating the params inputs with the default values found in the model."""
    return (model_rr["BW"],
            model_rr["fasting_glucose"],
            model_rr["fasting_insulin"],
            model_rr["fasting_NEFA"],
            model_rr["fasting_TG"],
            model_rr["mG"],
            model_rr["mTG"])


@callback(
    Output(ids.RESULTS_PLOTS, "figure"),
    Input(ids.RUN_SIMULATION_BUTTON, 'n_clicks'),
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
def run_simulation(_,
                   body_mass,
                   fasting_glucose,
                   fasting_insulin,
                   fasting_nefa,
                   fasting_tg,
                   meal_glucose,
                   meal_tg,
                   start_time,
                   stop_time,
                   steps):
    """Run the simulation using the set parameters."""
    global model_rr

    model_rr["BW"] = body_mass
    model_rr["fasting_glucose"] = fasting_glucose
    model_rr["fasting_insulin"] = fasting_insulin
    model_rr["fasting_NEFA"] = fasting_nefa
    model_rr["fasting_TG"] = fasting_tg
    model_rr["mG"] = meal_glucose
    model_rr["mTG"] = meal_tg

    _s = model_rr.simulate(start=start_time,
                      end=stop_time,
                      steps=steps)

    df = pd.DataFrame(_s, columns=_s.colnames)

    fig = make_subplots(rows=7, cols=3)

    fig.add_trace(
        go.Scatter(y=df["[g_gut]"]),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(y=df["[g_plasma]"]),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(y=df["[g_integral]"]),
        row=1, col=3
    )

    fig.add_trace(
        go.Scatter(y=df["[I_PL]"]),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(y=df["[i_intestitial]"]),
        row=2, col=2
    )

    fig.add_trace(
        go.Scatter(y=df["[i_delay1]"]),
        row=2, col=3
    )

    fig.add_trace(
        go.Scatter(y=df["[i_delay2]"]),
        row=3, col=1
    )

    fig.add_trace(
        go.Scatter(y=df["[i_delay3]"]),
        row=3, col=2
    )

    fig.add_trace(
        go.Scatter(y=df["[nefa_plasma]"]),
        row=3, col=3
    )

    fig.add_trace(
        go.Scatter(y=df["[tg_gut]"]),
        row=4, col=1
    )

    fig.add_trace(
        go.Scatter(y=df["[tg_delay1]"]),
        row=4, col=2
    )

    fig.add_trace(
        go.Scatter(y=df["[tg_delay2]"]),
        row=4, col=3
    )

    fig.add_trace(
        go.Scatter(y=df["[tg_plasma]"]),
        row=5, col=1
    )

    return fig


