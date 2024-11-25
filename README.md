# Indoor Temperature Control using Model Predictive Control (MPC)

This project demonstrates the use of Model Predictive Control (MPC) to regulate indoor temperature within a comfortable range by controlling a heater. The objective is to minimize energy consumption while maintaining a desired temperature setpoint.

## Key Features

1. **Prediction Horizon:** A prediction horizon (`N`) of 48 steps is used to plan control actions over the next 24 hours.
2. **Optimization:** The control problem is formulated as a quadratic optimization problem solved using the CVXPY library.
3. **Dynamic Modeling:** The system considers dynamics such as heating power, cooling rate, and the influence of outdoor temperature.
4. **Constraints:** Includes comfort temperature bounds, heater power limits, and system dynamics constraints.
5. **Cost Function:** Balances energy cost and penalties for deviation from the desired temperature.

## Requirements

- Python 3.x
- Libraries: 
  - `cvxpy`: Optimization solver for MPC
  - `numpy`: Numerical computations
  - `matplotlib`: Data visualization

Install the required libraries using:
```bash
pip install cvxpy numpy matplotlib
```

## Code Overview

### Parameters
- **`N`**: Prediction horizon.
- **`T_desired`**: Desired indoor temperature in °C.
- **`x_min`, `x_max`**: Bounds for the comfort temperature range.
- **`u_max`**: Maximum heating power.
- **`c`, `q`**: Cost weights for heater power usage and temperature deviation penalties.

### Dynamics
- **Heating Effect (`a`)**: Impact of the heater on temperature.
- **Cooling Rate (`b`)**: Natural cooling of the environment.
- **Outdoor Temperature (`w`)**: Assumed constant for simplicity.

### Optimization Problem
The MPC problem optimizes:
\[ \text{Cost} = \sum_{t=0}^{N-1} \big(c \cdot u_t^2 + q \cdot (x_t - T_{\text{desired}})^2\big) \]
Subject to:
- State and input constraints (comfort range and heater power limits).
- System dynamics constraints.

### Simulation Loop
The control actions are computed iteratively over the prediction horizon:
1. Solve the optimization problem for the current state.
2. Apply the first control action.
3. Update the temperature based on system dynamics.
4. Store results for analysis.

### Results Visualization
The results include:
- **Temperature Plot**: Indoor temperature over time compared to the desired setpoint and comfort bounds.
- **Heater Power Plot**: Heating power applied over time.

## Usage

1. Run the script in a Python environment.
2. The script outputs two plots:
   - Indoor temperature profile.
   - Heater power usage.
3. Modify parameters like `N`, `T_desired`, and `x0` to test different scenarios.

## Output
- **Temperature Control**: Maintains indoor temperature within the desired comfort range.
- **Heater Efficiency**: Optimized power usage to minimize energy costs.

This project showcases a simple yet effective application of MPC for home temperature regulation. It's a starting point for more complex scenarios, such as time-varying outdoor temperatures or multi-zone heating systems.
