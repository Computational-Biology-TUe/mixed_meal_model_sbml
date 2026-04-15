from importlib.metadata import version
import dash_bootstrap_components as dbc
from dash import html
from dash import page_container
from meal_model_dashboard.app import app
from meal_model_dashboard.callbacks import model_load_callbacks  # noqa: F401
from meal_model_dashboard.definitions import layout_styles as styles

app.layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H1("MixedMealModel Studio", style=styles.MAIN_TITLE_STYLE),
                                html.P(
                                    (
                                        "Professional dashboard for loading, configuring, and simulating "
                                        "postprandial metabolic dynamics."
                                    ),
                                    className="text-center text-muted mb-1",
                                ),
                            ],
                            lg=8,
                        ),
                        dbc.Col(
                            [html.Div(f"Version {version('mixed_meal_model_sbml')}", style=styles.VERSION)],
                            lg=4,
                            className="d-flex align-items-center justify-content-lg-end justify-content-center",
                        ),
                    ],
                    className="py-4 border-bottom",
                ),
                dbc.Row([dbc.Col(page_container)]),
            ],
            fluid="lg",
            className="pb-4",
        )
    ],
    className="bg-light min-vh-100",
)

if __name__ == "__main__":
    app.run_server(debug=False)
