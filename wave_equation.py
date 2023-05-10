import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import spectral

# Define initial condition
initial_conditions = {
	1: 'positive-positive',
	2: 'positive-negative'
}
initial_choice = int(input(
	'Choose a initial condition: \n\t(1) positive-positive\n\t(2) positive-negative\n1/2: '
))
if initial_choice not in initial_conditions.keys():
	print('Error: invalid initial condition!')
	exit(1)

# Define boundary conditions
boundary_conditions = {
	1: ['none', 'none'],
	2: ['soft-soft', 'left = soft; right = soft'],
	3: ['soft-hard', 'left = soft; right = hard'],
	4: ['hard-hard', 'left = hard; right = hard'],
}
boundary_choice = int(input(
	'Choose a boundary condition: \n\t(1) none\n\t(2) soft-soft\n\t(3) soft-hard\n\t(4) hard-hard\n1/2/3/4: '
))
if boundary_choice not in boundary_conditions.keys():
	print('Error: invalid boundary condition!')
	exit(1)

# Define grid
N = 1001
x_min = 0
x_max = 10
x, Delta = spectral.grid(N, x_min, x_max)

# Right sides of PDEs
def f(psi, u_plus, u_minus):
	psi_dot = 1/2 * (u_plus + u_minus)
	u_plus_dot = spectral.derivative(u_plus)
	u_minus_dot = - spectral.derivative(u_minus)
	return psi_dot, u_plus_dot, u_minus_dot

# Enforce initial value
if initial_choice == 1: # positive-positive
	psi = np.exp(- (x - x_max/2)**2)
	pi = np.zeros_like(psi)
	phi = spectral.derivative(psi)
	u_plus = pi + phi
	u_minus = pi - phi
elif initial_choice == 2: # positive-negative
	psi = np.zeros_like(x)
	u_plus = .5 * np.exp(- (x - x_max/2)**2)
	u_minus = - .5 * np.exp(- (x - x_max/2)**2)

# Set up logs for animation
solution_log = np.zeros((1, N))
solution_log[0,:] = psi[:]

# RK-4 time-stepping
dt = 0.01
final_time = 30
N_frames = 1000
N_steps = int(final_time / dt)
N_steps_per_frame = N_steps / N_frames
for step in range(N_steps):
	k1_psi, k1_u_plus, k1_u_minus = f(psi, u_plus, u_minus)
	k2_psi, k2_u_plus, k2_u_minus = f(psi + 1/2 * dt * k1_psi, u_plus + 1/2 * dt * k1_u_plus, u_minus + 1/2 * dt * k1_u_minus)
	k3_psi, k3_u_plus, k3_u_minus = f(psi + 1/2 * dt * k2_psi, u_plus + 1/2 * dt * k2_u_plus, u_minus + 1/2 * dt * k2_u_minus)
	k4_psi, k4_u_plus, k4_u_minus = f(psi + dt * k3_psi, u_plus + dt * k3_u_plus, u_minus + dt * k3_u_minus)

	psi += dt * 1/6 * (k1_psi + 2*k2_psi + 2*k3_psi + k4_psi)
	u_plus += dt * 1/6 * (k1_u_plus + 2*k2_u_plus + 2*k3_u_plus + k4_u_plus)
	u_minus += dt * 1/6 * (k1_u_minus + 2*k2_u_minus + 2*k3_u_minus + k4_u_minus)

	# Enforce boundary conditions
	if initial_choice == 1: # positive-positive
		if boundary_choice == 2:
			u_minus[0] = u_plus[0] # left = soft
			u_plus[-1] = u_minus[-1] # right = soft
		elif boundary_choice == 3:
			u_minus[0] = u_plus[0] # left = soft
			u_plus[-1] = - u_minus[-1] # right = hard
		elif boundary_choice == 4:
			u_minus[0] = - u_plus[0] # left = hard
			u_plus[-1] = - u_minus[-1] # right = hard
	elif initial_choice == 2: # positive-negative
		if boundary_choice == 2:
			u_minus[0] = - u_plus[0] # left = soft
			u_plus[-1] = - u_minus[-1] # right = soft
		elif boundary_choice == 3:
			u_minus[0] = - u_plus[0] # left = soft
			u_plus[-1] = u_minus[-1] # right = hard
		elif boundary_choice == 4:
			u_minus[0] = u_plus[0] # left = hard
			u_plus[-1] = u_minus[-1] # right = hard

	psi = spectral.filter(psi)
	u_plus = spectral.filter(u_plus)
	u_minus = spectral.filter(u_minus)
	
	if step % N_steps_per_frame == 0:
		solution_log = np.vstack((solution_log, psi))
	if step % 500 == 0:
		print(f'{step / N_steps * 100}%')

# Show animation
fig, ax = plt.subplots()
line, = ax.plot(x, solution_log[0,:])
plt.title(f'Boundary conditions: {boundary_conditions[boundary_choice][1]}')

if initial_choice == 1: # positive-positive
	plt.ylim(-1.5, 1.5)
elif initial_choice == 2: # positive-negative
	plt.ylim(-2, 2)

def animate(i):
	line.set_ydata(solution_log[i,:])
	return line,

ani = FuncAnimation(fig, animate, frames=len(solution_log), interval=10)
ani.save(f'assets/{initial_conditions[initial_choice]}_{boundary_conditions[boundary_choice][0]}_{N}.gif', dpi=200, fps=30)

plt.show()
