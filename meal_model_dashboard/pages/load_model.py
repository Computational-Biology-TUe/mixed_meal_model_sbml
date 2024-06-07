import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import register_page
import meal_model_dashboard.definitions.element_ids as ids
import meal_model_dashboard.definitions.layout_styles as styles

register_page(__name__, path="/")

model_upload = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Upload(
                            id=ids.UPLOAD_MODEL,
                            children=html.Div(["Drag and Drop or ", html.A("Select Model File")]),
                            accept="text/xml",
                            style=styles.UPLOAD_BUTTON,
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Div("OR", style=styles.TEXT_STYLE),
                    ],
                    style=styles.COLUMN,
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            id=ids.CREATE_MODEL_BUTTON,
                            children=["CREATE MODEL"],
                            style=styles.MODEL_BUTTON,
                        ),
                    ],
                    style=styles.COLUMN,
                ),
            ]
        ),
        html.P(),
        html.Div(id=ids.ERROR_MESSAGE),
        dbc.Row(
            [
                html.Div(
                    [
                        dbc.Row(
                            [
                                html.H3("Set the model parameters"),
                            ],
                            style=styles.MAIN_TITLE_STYLE,
                        ),
                        html.P(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.P("Meal glucose mass [mg]"),
                                        dbc.Input(id=ids.MEAL_GLUCOSE_INPUT, type="number", min=0),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.P("Meal TG mass [mg]"),
                                        dbc.Input(id=ids.MEAL_TG_INPUT, type="number", min=0),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.P("Subject body mass [Kg]"),
                                        dbc.Input(id=ids.BODY_MASS_INPUT, type="number", min=0),
                                    ]
                                ),
                            ]
                        ),
                        html.P(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.P("Fasting glucose [mmol]"),
                                        dbc.Input(id=ids.FASTING_GLUCOSE_INPUT, type="number",
                                                  min=0),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.P("Fasting insulin [μIU/ml]"),
                                        dbc.Input(id=ids.FASTING_INSULIN_INPUT, type="number",
                                                  min=0),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.P("Fasting TG [mmol]"),
                                        dbc.Input(id=ids.FASTING_TG_INPUT, type="number", min=0),
                                    ]
                                ),
                            ]
                        ),
                        html.P(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.P("Fasting NEFA [mmol]"),
                                        dbc.Input(id=ids.FASTING_NEFA_INPUT, type="number", min=0),
                                    ]
                                ),
                                dbc.Col(),
                                dbc.Col(),
                            ]
                        ),
                        html.P(),
                        dbc.Row(
                            [
                                html.H3("Set the simulation time"),
                            ],
                            style=styles.MAIN_TITLE_STYLE,
                        ),
                        html.P(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.P("Starting time [min]"),
                                        dbc.Input(id=ids.START_TIME_INPUT, type="number", min=0,
                                                  value=0),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.P("Stop time [min]"),
                                        dbc.Input(id=ids.STOP_TIME_INPUT, type="number", min=0,
                                                  value=500),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.P("Steps number"),
                                        dbc.Input(id=ids.STEPS_TIME_INPUT, type="number", min=0,
                                                  value=500),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    id=ids.PARAMETERS_CONTAINER,
                    hidden=True,
                ),
            ]
        ),
        html.P(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button(
                            "RUN SIMULATION", id=ids.RUN_SIMULATION_BUTTON,
                            style=styles.MODEL_BUTTON, disabled=True
                        ),
                    ],
                    style=styles.COLUMN,
                )
            ]
        ),
        dcc.Graph(id=ids.RESULTS_PLOTS, style=styles.EMPTY_ELEMENT),
        html.Div([], id="test"),
        html.P(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Button(
                                    "DOWNLOAD RESULTS", id=ids.DOWNLOAD_RESULTS_BUTTON,
                                    style=styles.MODEL_BUTTON
                                ),
                                dcc.Download(id=ids.DOWNLOAD_RESULTS),
                            ],
                            id=ids.DOWNLOAD_RESULTS_DIV,
                            hidden=True
                        ),
                    ],
                    style=styles.COLUMN,
                )
            ]
        ),
    ]
)

layout = dbc.Row([model_upload])
