# Constitutive Law Optimizer

This is a project to define the optimal material parameters to obtain the desired material behaviour.

### Procedure:
1. Generate various different parameter combinations within a uniform distribution range for each.
2. Run the desired simulations with the given parameter combinations.
3. Extract the desired information from the results to quantify the outcomes.
4. Train a regression model with the parameter combinations and the corresponding extracted results.
5. Predict the parameter combination that would result in the desired outcome in the simulation.

## Example Simulation: Granular Flow Simulation

This example was done using the Particle Mechanics Application of the [@KratosMultiphysics](https://github.com/KratosMultiphysics/Kratos) framework to simulate granular flow. The result of the simulation is quantified by measuring the y-coordinate of the slope at specific points. The example can be seen in the figure below.

Start:
![start](https://user-images.githubusercontent.com/73847250/221851535-5129ef9d-af96-4a77-95cc-8b528300bb06.png)
End:
![end](https://user-images.githubusercontent.com/73847250/221851581-033caa33-5785-42f8-b55c-052843152d6d.png)
