import warnings

import click

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=UserWarning)
    from mixed_meal_model_sbml import create_sbml_model
    from mixed_meal_model_sbml import run_simulation
    from mixed_meal_model_sbml import MODEL_PATH

from meal_model_dashboard.app import app


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Default prompt. It shows the help command"""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command(name="create-model", help="Create and save the SBML model.")
@click.option('--path', help="Location where the model will be saved. "
                             "The path must include the file name (e.g., model.xml)",
              type=str, default=MODEL_PATH, show_default=True)
def create_model(path):
    """Create and save the SBML model."""
    path = path or MODEL_PATH
    model = create_sbml_model(path)

    try:
        open(model.sbml_path)
        msg = f"Model saved in {model.sbml_path}"
    except FileNotFoundError:
        msg = f"The path specified is not valid: {path}"

    click.echo(msg)


@cli.command(name="run-simulation", help="Run the simulation of the SBML model.")
@click.option('--file-path', help="Path to the SBML model.", type=str)
@click.option('--start-time', help="Start time of the simulation.", type=int)
@click.option('--end-time', help="End time of the simulation.", type=int)
@click.option('--steps', help="Number of steps between the start and end time.", type=int)
@click.option('--save-path', help="Path where to save the results.", type=str)
def simulate(file_path, start_time, end_time, steps, save_path):
    """Run the simulation of the SBML model."""
    try:
        open(file_path)
    except FileNotFoundError:
        msg = f"The path specified is not valid: {file_path}"
        click.echo(msg)

    try:
        start_time = int(start_time)
        end_time = int(end_time)
        steps = int(steps)
    except TypeError:
        msg = "The start-time, end-time and steps must be integer"
        click.echo(msg)

    res = run_simulation(file_path, start_time, end_time, steps)
    res.to_csv(save_path)
    msg = f"File saved in {save_path}"

    click.echo(msg)


@cli.command(name="run-dashboard", help="Start the dashboard.")
def run_dashboard():
    """Start the dashboard."""

    app.run_server(debug=False)


if __name__ == '__main__':
    cli()
