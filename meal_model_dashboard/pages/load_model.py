import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import register_page
import meal_model_dashboard.definitions.element_ids as ids
import meal_model_dashboard.definitions.layout_styles as styles

register_page(__name__, path="/")

def parameter_input(label: str, input_id: str) -> dbc.Col:
    return dbc.Col(
        [
            dbc.Label(label, html_for=input_id, className="fw-semibold text-secondary"),
            dbc.Input(id=input_id, type="number", min=0),
        ],
        md=6,
        lg=4,
        className="mb-3",
    )


model_upload = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Load or Generate Model", className="card-title"),
                                html.P(
                                    "Upload a MixedMealModel SBML file or generate a reference model instantly.",
                                    className="text-muted mb-4",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Upload(
                                                id=ids.UPLOAD_MODEL,
                                                children=html.Div(
                                                    [
                                                        html.I(className="fas fa-cloud-upload-alt me-2"),
                                                        "Drag and drop or select XML file",
                                                    ]
                                                ),
                                                accept="text/xml",
                                                style=styles.UPLOAD_BUTTON,
                                            ),
                                            md=7,
                                        ),
                                        dbc.Col(
                                            html.Div("OR", style=styles.TEXT_STYLE),
                                            md=1,
                                            className="d-flex align-items-center justify-content-center",
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                id=ids.CREATE_MODEL_BUTTON,
                                                children=["Create model from defaults"],
                                                style=styles.MODEL_BUTTON,
                                                color="primary",
                                                className="w-100",
                                            ),
                                            md=4,
                                            className="d-flex align-items-center",
                                        ),
                                    ],
                                    className="g-3",
                                ),
                                html.Div(id=ids.ERROR_MESSAGE, className="text-danger fw-semibold mt-3"),
                            ]
                        ),
                        className="shadow-sm border-0",
                    ),
                    width=12,
                    className="mb-4",
                ),
            ]
        ),
        html.Div(
            id=ids.PARAMETERS_CONTAINER,
            hidden=True,
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H4("Model Parameters", className="card-title"),
                                        html.P(
                                            "Tune subject and fasting state assumptions before simulation.",
                                            className="text-muted mb-4",
                                        ),
                                        dbc.Row(
                                            [
                                                parameter_input("Meal glucose mass [mg]", ids.MEAL_GLUCOSE_INPUT),
                                                parameter_input("Meal TG mass [mg]", ids.MEAL_TG_INPUT),
                                                parameter_input("Subject body mass [kg]", ids.BODY_MASS_INPUT),
                                                parameter_input("Fasting glucose [mmol]", ids.FASTING_GLUCOSE_INPUT),
                                                parameter_input("Fasting insulin [uIU/ml]", ids.FASTING_INSULIN_INPUT),
                                                parameter_input("Fasting TG [mmol]", ids.FASTING_TG_INPUT),
                                                parameter_input("Fasting NEFA [mmol]", ids.FASTING_NEFA_INPUT),
                                            ]
                                        ),
                                    ]
                                ),
                                className="shadow-sm border-0 h-100",
                            ),
                            lg=8,
                            className="mb-4",
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H4("Simulation Window", className="card-title"),
                                        html.P(
                                            "Define the simulation horizon and temporal resolution.",
                                            className="text-muted mb-4",
                                        ),
                                        dbc.Label("Start time [min]", html_for=ids.START_TIME_INPUT, className="fw-semibold text-secondary"),
                                        dbc.Input(id=ids.START_TIME_INPUT, type="number", min=0, value=0, className="mb-3"),
                                        dbc.Label("Stop time [min]", html_for=ids.STOP_TIME_INPUT, className="fw-semibold text-secondary"),
                                        dbc.Input(id=ids.STOP_TIME_INPUT, type="number", min=0, value=500, className="mb-3"),
                                        dbc.Label("Number of steps", html_for=ids.STEPS_TIME_INPUT, className="fw-semibold text-secondary"),
                                        dbc.Input(id=ids.STEPS_TIME_INPUT, type="number", min=0, value=500, className="mb-4"),
                                        dbc.Button(
                                            "Run simulation",
                                            id=ids.RUN_SIMULATION_BUTTON,
                                            style=styles.MODEL_BUTTON,
                                            color="success",
                                            className="w-100",
                                            disabled=True,
                                        ),
                                    ]
                                ),
                                className="shadow-sm border-0 h-100",
                            ),
                            lg=4,
                            className="mb-4",
                        ),
                    ]
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Simulation Results", className="card-title"),
                                html.P("Plots update after each successful simulation run.", className="text-muted mb-4"),
                                dcc.Graph(id=ids.RESULTS_PLOTS, style=styles.EMPTY_ELEMENT),
                                html.Div(
                                    [
                                        dbc.Button(
                                            "Download results",
                                            id=ids.DOWNLOAD_RESULTS_BUTTON,
                                            style=styles.MODEL_BUTTON,
                                            color="secondary",
                                        ),
                                        dcc.Download(id=ids.DOWNLOAD_RESULTS),
                                    ],
                                    id=ids.DOWNLOAD_RESULTS_DIV,
                                    hidden=True,
                                    className="mt-2 text-center",
                                ),
                            ]
                        ),
                        className="shadow-sm border-0",
                    ),
                    width=12,
                )
            ]
        ),
    ],
    fluid=True,
    className="pt-4",
)

layout = dbc.Row([model_upload])
