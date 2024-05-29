from dash import html
from dash import page_container
from meal_model_dashboard.app import app
from meal_model_dashboard.callbacks import model_load_callbacks  # noqa: F401
from meal_model_dashboard.definitions import layout_styles as styles

app.layout = html.Div(
    [
        html.H1(
            children="MixedMealModel dashboard",
            style=styles.MAIN_TITLE_STYLE,
        ),
        page_container,
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True)
