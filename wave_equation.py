import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import spectral

# Define grid
N = 101
x_min = 0
x_max = 10
x, Delta = spectral.grid(N, x_min, x_max)

# Right sides of PDEs
def f(psi, u_plus, u_minus):
	psi_dot = 1/2 * (u_plus + u_minus)
	u_plus_dot = spectral.derivative(u_plus)
	u_minus_dot = - spectral.derivative(u_minus)
	return psi_dot, u_plus_dot, u_minus_dot

# Initial value
psi = np.exp(- (x - x_max/2)**2)
pi = np.zeros_like(psi)
phi = spectral.derivative(psi)

# Set up logs for animation
solution_log = np.zeros((1, N))
solution_log[0,:] = psi[:]

# Characteristic decomposition
u_plus = pi + phi
u_minus = pi - phi

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

	# Soft reflection
	u_minus[0] = u_plus[0] # left
	# u_plus[-1] = u_minus[-1] # right

	# Hard reflection
	# u_minus[0] = - u_plus[0] # left
	u_plus[-1] = - u_minus[-1] # right
	
	if step % N_steps_per_frame == 0:
		solution_log = np.vstack((solution_log, psi))
	if step % 500 == 0:
		print(f'{step / N_steps * 100}%')

# Show animation
fig, ax = plt.subplots()
line, = ax.plot(x, solution_log[0,:])
plt.title('Boundary conditions: left = soft; right = hard')
plt.ylim(-10, 10)

def animate(i):
	line.set_ydata(solution_log[i,:])
	return line,

ani = FuncAnimation(fig, animate, frames=len(solution_log), interval=10)
# ani.save(f'assets/soft-hard_{N}.gif', dpi=200)

plt.show()
