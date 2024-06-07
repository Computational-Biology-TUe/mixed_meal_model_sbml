# User manual for MixedMealModel dashboard

Note 1: If you have not installed the dashboard yet, please refer to our [README](../../README.md) on instructions how to do
that.

Note 2: While the dashboard is rendered in a browser window, you are not working online. All data that you load into the
dashboard remains local on your machine.

## Uploading or generating a model

When opening the dashboard the following page will be displayed:

<kbd>
<img src=images/initial_page.png width="1200px">
</kbd>

An existing SBML model can be uploaded using the `Drag and Drop or Select Model File`, 
by clicking on the button and navigating to the desired file or by dragging a dropping it on the button area.

N.B. Only `.xml` files can be uploaded, and only the MixedMealModel can be used.
Other SBML models will not be correctly loaded.

In case a local SBML model is not available, it can be generated using the `CREARTE MODEL` button.
This will generate a model using the [codebase](../../mixed_meal_model_sbml) and use it.

## Setting the model and simulation parameters

After uploading or generating a model, the list of adjustable parameters will be displayed.

<kbd>
<img src=images/set_parameters.png width="1200px">
</kbd>

The default values are already set for all the parameters at loading time, but all the displayed
parameters are adjustable, both for the model and the simulation time.

## Running a simulation

When all the parameters have been set, a simulation can be run by clicking on the `RUN SIMULATION` button.
The simulation results will be displayed as shown here below.

<kbd>
<img src=images/simulation_results.png width="1200px">
</kbd>
