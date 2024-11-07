import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt

# Parameters
N = 48               # Prediction horizon (e.g., 24 hours)
T_desired = 20       # Desired temperature in Celsius
x_min, x_max = 16, 24  # Comfort temperature bounds
u_max = 1.5            # Max power of the heater (0 to 1 scale)
c = 1                # Cost per unit of heater power
q = 2                # Penalty for deviation from T_desired

# System dynamics constants
a = 0.5              # Heating effect from the heater
b = 0.07             # Cooling rate
w = 5                # Outdoor temperature (constant for simplicity)

# Initial indoor temperature
x0 = 16              # Initial temperature, below the comfort range

# Initialize lists to store results
x_vals = [x0]
u_vals = []

# Define MPC loop
for k in range(N):
    # Define optimization variables for MPC over the horizon
    u = cp.Variable(N)
    x = cp.Variable(N+1)
    
    # Objective function (cost function)
    cost = 0
    constraints = []
    constraints += [x[0] == x_vals[-1]]  # Initial state constraint
    
    # Define cost function and constraints over the prediction horizon
    for t in range(N):
        # Cost includes heating cost and deviation penalty
        cost += c * cp.square(u[t]) + q * cp.square(x[t] - T_desired)
        
        # System dynamics constraint
        constraints += [x[t+1] == x[t] + a * u[t] - b * (x[t] - w)]
        
        # Input and state constraints
        constraints += [0 <= u[t], u[t] <= u_max]       # Power limits
        constraints += [x_min <= x[t+1], x[t+1] <= x_max]  # Temperature comfort range

    # Define optimization problem
    problem = cp.Problem(cp.Minimize(cost), constraints)
    problem.solve()

    # Check if the problem was solved successfully
    if problem.status == cp.OPTIMAL:
        # Extract the first optimal control action and apply it
        u_opt = u.value[0]  # Optimal control action at current step
    else:
        print("Optimization problem is not solved. Status:", problem.status)
        u_opt = 0  # Default action if optimization fails

    x_next = x_vals[-1] + a * u_opt - b * (x_vals[-1] - w)  # Update temperature based on dynamics

    # Store results
    u_vals.append(u_opt)
    x_vals.append(x_next)

# Plot the results
time = np.arange(N+1)
plt.figure(figsize=(12, 5))
plt.subplot(2, 1, 1)
plt.plot(time, x_vals, label="Indoor Temperature")
plt.axhline(T_desired, color='r', linestyle="--", label="Desired Temp (20°C)")
plt.fill_between(time, x_min, x_max, color='orange', alpha=0.1, label="Comfort Range")
plt.xlabel("Time (Hours)")
plt.ylabel("Temperature (°C)")
plt.legend()

plt.subplot(2, 1, 2)
plt.step(time[:-1], u_vals, where="post", label="Heater Power (u)")
plt.xlabel("Time (Hours)")
plt.ylabel("Heater Power")
plt.ylim(0, 1)
plt.legend()

plt.tight_layout()
plt.show()
