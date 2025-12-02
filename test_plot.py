from backend.plot import plot_simulation
from config import simulation_file_path
import os
path = os.path.join(simulation_file_path,"001.json")
plot_simulation(path)