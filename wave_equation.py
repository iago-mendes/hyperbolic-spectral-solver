import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import spectral

# Define grid
N = 100
x_min = 0
x_max = 10
x = np.linspace(x_min, x_max, N, endpoint=False)
Delta = (x_max - x_min) / N

# Right side of PDE
def f(u):
	v = - 5 # speed
	return v * spectral.derivative(u, N, Delta)

# Set up logs for animation
solution_log = np.zeros((1, N))

# Initial value
u = np.exp(- (x - x_max/2)**2)
solution_log[0,:] = u[:]

# RK-4 time-stepping
dt = 0.01
final_time = 5
N_frames = 1000
N_steps = int(final_time / dt)
N_steps_per_frame = N_steps / N_frames
for step in range(N_steps):
	k1 = f(u)
	k2 = f(u + 1/2 * dt * k1)
	k3 = f(u + 1/2 * dt * k2)
	k4 = f(u + dt * k3)

	u = u + dt * 1/6 * (k1 + 2*k2 + 2*k3 + k4)
	
	if step % N_steps_per_frame == 0:
		solution_log = np.vstack((solution_log, u))
	if step % 100 == 0:
		print(f'{step / N_steps * 100}%')

# Show animation
fig, ax = plt.subplots()
line, = ax.plot(x, solution_log[0,:])

def animate(i):
	line.set_ydata(solution_log[i,:])
	return line,

ani = FuncAnimation(fig, animate, frames=len(solution_log), interval=10)
plt.show()
