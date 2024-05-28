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
                dcc.Upload(
                    id=ids.UPLOAD_MODEL,
                    children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
                    accept="text/xml",
                    style={
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "margin": "10px",
                    },
                ),
            ]
        ),
        html.P(),
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
                                        dbc.Input(id=ids.FASTING_GLUCOSE_INPUT, type="number", min=0),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.P("Fasting insulin [μIU/ml]"),
                                        dbc.Input(id=ids.FASTING_INSULIN_INPUT, type="number", min=0),
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
                                        html.P("Starting time [s]"),
                                        dbc.Input(id=ids.START_TIME_INPUT, type="number", min=0, value=0),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.P("Stop time [s]"),
                                        dbc.Input(id=ids.STOP_TIME_INPUT, type="number", min=0, value=500),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.P("Steps number"),
                                        dbc.Input(id=ids.STEPS_TIME_INPUT, type="number", min=0, value=500),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    id=ids.PARAMETERS_CONTAINER,
                ),
            ]
        ),
        html.P(),
        dbc.Row(
            [
                dbc.Button("RUN SIMULATION", id=ids.RUN_SIMULATION_BUTTON, disabled=True),
            ]
        ),
        dcc.Graph(id=ids.RESULTS_PLOTS, style=styles.EMPTY_ELEMENT),
        html.Div([], id="test"),
    ]
)

layout = dbc.Row([model_upload])
