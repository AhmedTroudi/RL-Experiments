import tkinter as tk
import argparse
from gui import RobotGUI
from dyna_q import DynaQ
from environment import Environment
from helper import read_csv


def main():
    parser = argparse.ArgumentParser(description="Robot path finding "
                                     "simulation with Dyna-Q learning")
    parser.add_argument("--filename", type=str, default="maps/map_01.csv",
                        help="Path to the map file")
    parser.add_argument("--epochs", type=int, default=150,
                        help="Number of epochs for the simulation")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose mode")
    parser.add_argument("--dyna", type=int, default=0, help="Enable Dyna")
    args = parser.parse_args()

    # Load the map
    map_layout = read_csv(args.filename)

    # Create an environment
    environment = Environment(map_layout)

    # Initialize UI
    root = tk.Tk()
    root.title("Robot GUI")
    robot_gui = RobotGUI(root, map_layout, environment.start_position,
                         environment.goal_position)

    learner = DynaQ(num_states=150, num_actions=4, alpha=0.2, epsilon=0.9999,
                    epsilon_decay=0.99999, gamma=0.9, dyna=args.dyna,
                    verbose=False)

    total_reward = environment.run_episode(args.epochs, learner, args.verbose)

    for move in environment.robot_moves:
        robot_gui.move_robot(move)
        root.update_idletasks()
        root.update()
        # Adjust the delay (in milliseconds) to control the speed of the visualization
        root.after(200)

    root.mainloop()
    if args.verbose:
        print(f"{args.epochs}, median total_reward {total_reward}")


if __name__ == "__main__":
    main()
