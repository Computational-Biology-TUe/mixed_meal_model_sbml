from importlib.metadata import version
import dash_bootstrap_components as dbc
from dash import html
from dash import page_container
from meal_model_dashboard.app import app
from meal_model_dashboard.callbacks import model_load_callbacks  # noqa: F401
from meal_model_dashboard.definitions import layout_styles as styles

app.layout = html.Div(
    [
        dbc.Col(
            [
                dbc.Row(
                    [
                        html.H1(
                            children="MixedMealModel dashboard",
                            style=styles.MAIN_TITLE_STYLE,
                        ),
                    ]
                ),
                dbc.Row([html.Div(f"Version {version('mixed_meal_model_sbml')}", style=styles.VERSION)]),
            ]
        ),
        page_container,
    ],
)

if __name__ == "__main__":
    app.run_server(debug=False)
