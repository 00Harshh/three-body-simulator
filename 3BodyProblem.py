import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

# Physical Constants 
G = 6.67430e-11  # Gravitational constant (m³/kg⋅s²)
AU = 1.496e11    # Astronomical Unit in meters
SOLAR_MASS = 1.989e30  # Solar mass in kg
DAY = 24 * 3600  # One day in seconds

# Scaling factors for simulation
MASS_SCALE = SOLAR_MASS
DISTANCE_SCALE = AU
TIME_SCALE = DAY * 1  #time scale (1 unit = 1 day)

# Scaled gravitational constant
G_scaled = G * MASS_SCALE * (TIME_SCALE**2) / (DISTANCE_SCALE**3)

class ThreeBodySimulator:
    def __init__(self):
        
        self.masses = np.array([
            1.0,    # Central massive body 
            0.1,    # Medium body 
            0.05    # Small body 
        ]) * MASS_SCALE
        
        
        self.positions = np.array([
            [0.0, 0.0],      # Central body at origin
            [1.5, 0.0],      # Second body to the right
            [0.75, 1.3]      # Third body forming triangle
        ]) * DISTANCE_SCALE
        
        
        self.velocities = np.array([
            [0.0, 1.0],      # Central body with significant motion
            [0.0, -3.0],     # Second body very fast orbital motion
            [-2.5, 1.5]      # Third body very fast orbital motion
        ]) * np.sqrt(G_scaled * MASS_SCALE / DISTANCE_SCALE)
        
        self.adjust_center_of_mass()
        
        # Storage for trajectories and analysis
        self.trajectory_length = 500
        self.trajectories = [deque(maxlen=self.trajectory_length) for _ in range(3)]
        
        
        self.dt = TIME_SCALE * 100  # 100 days per step
        self.time = 0.0
        
        # Chaos analysis parameters
        self.chaos_data = {
            'times': deque(maxlen=1000),
            'separations': deque(maxlen=1000),
            'lyapunov': deque(maxlen=1000),
        }
        
        self.initial_separation = np.linalg.norm(self.positions[1] - self.positions[2])
        
        
        self.colors = ['gold', 'red', 'blue']
        self.sizes = [20, 15, 12]  
        
    def adjust_center_of_mass(self):
        total_mass = np.sum(self.masses)
        com_pos = np.sum(self.masses[:, np.newaxis] * self.positions, axis=0) / total_mass
        com_vel = np.sum(self.masses[:, np.newaxis] * self.velocities, axis=0) / total_mass
        
        self.positions -= com_pos
        self.velocities -= com_vel
    
    def compute_accelerations(self):
        n = len(self.positions)
        accelerations = np.zeros((n, 2))
        for i in range(n):
            for j in range(n):
                if i != j:
                    r_vec = self.positions[j] - self.positions[i]
                    distance = np.linalg.norm(r_vec)
                    # Smaller softening for more realistic physics
                    softening = 0.0001 * DISTANCE_SCALE
                    distance_softened = np.sqrt(distance**2 + softening**2)
                    force_magnitude = G_scaled * self.masses[j] / distance_softened**3
                    accelerations[i] += force_magnitude * r_vec
        return accelerations
    
    def update_system(self):
        # Runge-Kutta 4th order integration for accuracy
        def derivatives(pos, vel):
            old_pos = self.positions.copy()
            self.positions[:] = pos
            acc = self.compute_accelerations()
            self.positions[:] = old_pos
            return vel, acc
        
        k1_pos, k1_vel = derivatives(self.positions, self.velocities)
        k2_pos, k2_vel = derivatives(self.positions + 0.5*self.dt*k1_pos, 
                                   self.velocities + 0.5*self.dt*k1_vel)
        k3_pos, k3_vel = derivatives(self.positions + 0.5*self.dt*k2_pos, 
                                   self.velocities + 0.5*self.dt*k2_vel)
        k4_pos, k4_vel = derivatives(self.positions + self.dt*k3_pos, 
                                   self.velocities + self.dt*k3_vel)
        
        self.positions += (self.dt/6) * (k1_pos + 2*k2_pos + 2*k3_pos + k4_pos)
        self.velocities += (self.dt/6) * (k1_vel + 2*k2_vel + 2*k3_vel + k4_vel)
        
        self.time += self.dt
        
        # Store trajectories
        for i in range(len(self.positions)):
            self.trajectories[i].append(self.positions[i].copy())
        
        self.analyze_chaos()
    
    def analyze_chaos(self):
        current_separation = np.linalg.norm(self.positions[1] - self.positions[2])
        self.chaos_data['times'].append(self.time / (DAY * 365.25))
        self.chaos_data['separations'].append(current_separation / self.initial_separation)
        
        if len(self.chaos_data['separations']) > 10:
            separations = np.array(list(self.chaos_data['separations']))
            valid_separations = separations[separations > 1e-10]
            if len(valid_separations) > 5:
                lyapunov = np.mean(np.diff(np.log(valid_separations)))
                self.chaos_data['lyapunov'].append(lyapunov)
            else:
                self.chaos_data['lyapunov'].append(0)
        else:
            self.chaos_data['lyapunov'].append(0)
    
    def get_energy(self):
        kinetic = 0.5 * np.sum(self.masses[:, np.newaxis] * self.velocities**2)
        potential = 0.0
        for i in range(len(self.masses)):
            for j in range(i+1, len(self.masses)):
                r = np.linalg.norm(self.positions[j] - self.positions[i])
                potential -= G_scaled * self.masses[i] * self.masses[j] / r
        return kinetic + potential


sim = ThreeBodySimulator()

# Setup plots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# Main simulation plot 
ax1.set_xlim(-3*AU, 3*AU)
ax1.set_ylim(-3*AU, 3*AU)
ax1.set_aspect('equal')
ax1.set_title('3-Body Motion', fontsize=14, fontweight='bold')
ax1.set_xlabel('Distance (AU)')
ax1.set_ylabel('Distance (AU)')
ax1.grid(True, alpha=0.3)

# Energy plot
ax2.set_title('Energy Conservation Check', fontsize=14)
ax2.set_xlabel('Time (years)')
ax2.set_ylabel('Total Energy')
ax2.grid(True, alpha=0.3)

# Chaos analysis plot
ax3.set_title('Separation Distance (Chaos Indicator)', fontsize=14)
ax3.set_xlabel('Time (years)')
ax3.set_ylabel('Separation Ratio')
ax3.grid(True, alpha=0.3)
ax3.set_yscale('log')

# Velocity plot (new - helps understand motion)
ax4.set_title('Body Velocities', fontsize=14)
ax4.set_xlabel('Time (years)')
ax4.set_ylabel('Speed (AU/year)')
ax4.grid(True, alpha=0.3)

# Initialize plot elements
bodies = []
trails = []
for i in range(3):
    body, = ax1.plot([], [], 'o', color=sim.colors[i], 
                     markersize=sim.sizes[i], label=f'Body {i+1} (M={sim.masses[i]/MASS_SCALE:.2f})')
    trail, = ax1.plot([], [], '-', color=sim.colors[i], alpha=0.7, linewidth=2)
    bodies.append(body)
    trails.append(trail)

ax1.legend(loc='upper right')

energy_line, = ax2.plot([], [], 'g-', linewidth=2, label='Total Energy')
ax2.legend()

separation_line, = ax3.plot([], [], 'r-', linewidth=2, label='Body 1-2 Separation')
ax3.legend()

# Velocity lines
velocity_lines = []
for i in range(3):
    line, = ax4.plot([], [], color=sim.colors[i], linewidth=2, label=f'Body {i+1}')
    velocity_lines.append(line)
ax4.legend()

# Text displays with better formatting
time_text = ax1.text(0.02, 0.98, '', transform=ax1.transAxes, 
                     fontsize=12, verticalalignment='top',
                     bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))

chaos_text = ax3.text(0.02, 0.02, '', transform=ax3.transAxes, 
                      fontsize=10, verticalalignment='bottom',
                      bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))

# Data storage
energy_times = deque(maxlen=2000)
energy_values = deque(maxlen=2000)
velocity_times = deque(maxlen=2000)
velocity_data = [deque(maxlen=2000) for _ in range(3)]

def init():
    for body in bodies:
        body.set_data([], [])
    for trail in trails:
        trail.set_data([], [])
    energy_line.set_data([], [])
    separation_line.set_data([], [])
    for line in velocity_lines:
        line.set_data([], [])
    time_text.set_text('')
    chaos_text.set_text('')
    return bodies + trails + [energy_line, separation_line] + velocity_lines + [time_text, chaos_text]

def animate(frame):
    # 50 updates per frame 
    for _ in range(50):
        sim.update_system()
    
    # Update body positions
    for i, body in enumerate(bodies):
        x, y = sim.positions[i]
        body.set_data([x/AU], [y/AU])
    
    # Update trails
    for i, trail in enumerate(trails):
        if len(sim.trajectories[i]) > 1:
            traj = np.array(list(sim.trajectories[i]))
            trail.set_data(traj[:, 0]/AU, traj[:, 1]/AU)
    
    # energy plot
    current_energy = sim.get_energy()
    energy_times.append(sim.time / (DAY * 365.25))
    energy_values.append(current_energy)
    
    if len(energy_times) > 1:
        energy_line.set_data(list(energy_times), list(energy_values))
        ax2.relim()
        ax2.autoscale_view()
    
    # separation plot
    if len(sim.chaos_data['times']) > 1:
        separation_line.set_data(list(sim.chaos_data['times']), 
                                list(sim.chaos_data['separations']))
        ax3.relim()
        ax3.autoscale_view()
    
    # velocity plot
    current_time = sim.time / (DAY * 365.25)
    velocity_times.append(current_time)
    for i in range(3):
        speed = np.linalg.norm(sim.velocities[i]) * (365.25 * DAY) / AU  # Convert to AU/year
        velocity_data[i].append(speed)
        if len(velocity_times) > 1:
            velocity_lines[i].set_data(list(velocity_times), list(velocity_data[i]))
    
    if len(velocity_times) > 1:
        ax4.relim()
        ax4.autoscale_view()
    
    #text displays
    years = sim.time / (DAY * 365.25)
    days = sim.time / DAY
    time_text.set_text(f'Time: {years:.2f} years\n({days:.0f} days)\nEnergy: {current_energy:.2e}')
    
    if len(sim.chaos_data['lyapunov']) > 0:
        avg_lyapunov = np.mean(list(sim.chaos_data['lyapunov'])[-10:])
        chaos_level = "HIGH" if avg_lyapunov > 0.01 else "MODERATE" if avg_lyapunov > 0.001 else "LOW"
        chaos_text.set_text(f'Chaos Level: {chaos_level}\nLyapunov: {avg_lyapunov:.4f}')
    
    return bodies + trails + [energy_line, separation_line] + velocity_lines + [time_text, chaos_text]

# Create animation
ani = FuncAnimation(fig, animate, frames=50000, init_func=init, 
                   blit=False, interval=10, repeat=True)  # 10ms = very fast refresh

plt.tight_layout()
plt.show()

print("=== U 3-Body Problem Simulation ===")
print(f"Time scale: 1 animation step = {sim.dt * 50 / DAY:.0f} days")
print(f"Animation speed: ~100 steps per second")
print(f"Real time ratio: 1 second of animation ≈ {sim.dt * 50 * 100 / (DAY * 365.25):.0f} years")
print()
print("What to observe:")
print("• Body movements and orbital patterns")
print("• How gravitational forces change trajectories")
print("• Energy conservation (should remain roughly constant)")
print("• Chaotic behavior (irregular, unpredictable motion)")
print("• Velocity changes as bodies interact")
print("=====================================")