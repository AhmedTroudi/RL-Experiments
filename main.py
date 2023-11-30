import numpy as np
import tkinter as tk
from gui import RobotGUI
from dyna_q import DynaQ
import argparse
from environment import Environment


def main():
    parser = argparse.ArgumentParser(description="Robot simulation with Dyna-Q learning")
    parser.add_argument("--filename", type=str, default="maps/map_01.csv", help="Path to the map file")
    parser.add_argument("--epochs", type=int, default=200, help="Number of epochs for the simulation")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose mode")
    args = parser.parse_args()

    # Load the map
    inf = open(args.filename)
    data = np.array([list(map(float, s.strip().split(","))) for s in inf.readlines()])

    # Create an environment
    environment = Environment(data)

    # Initialize UI
    root = tk.Tk()
    root.title("Robot GUI")
    robot_gui = RobotGUI(root, data)

    learner = DynaQ(num_states=150, num_actions=4, alpha=0.2, gamma=0.9, dyna=200, verbose=False)

    total_reward, robot_moves = environment.run_episode(args.epochs, learner, args.verbose)

    for move in robot_moves:
        robot_gui.move_robot(move)
        root.update_idletasks()
        root.update()
        root.after(500)  # Adjust the delay (in milliseconds) to control the speed of the visualization

    root.mainloop()
    if args.verbose:
        print(f"{args.epochs}, median total_reward {total_reward}")


if __name__ == "__main__":
    main()

