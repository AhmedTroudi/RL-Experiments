import tkinter as tk
import csv


class RobotGUI:
    def __init__(self, master, map_data, cell_size=100):
        self.master = master
        self.map_data = map_data
        self.rows = len(map_data)
        self.cols = len(map_data[0])
        self.cell_size = cell_size

        self.canvas_width = self.cols * self.cell_size
        self.canvas_height = self.rows * self.cell_size

        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        self.robot_position = None
        self.goal_position = None
        self.trail_positions = set()

        self.draw_map()

    def draw_map(self):
        self.canvas.delete("all")  # Clear the canvas

        for row in range(self.rows):
            for col in range(self.cols):
                cell_value = int(self.map_data[row][col])

                x1, y1 = col * 100, row * 100
                x2, y2 = x1 + 100, y1 + 100

                if cell_value == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')
                elif cell_value == 1:
                    self.robot_position = (row, col)
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='blue', outline='black')  # Robot
                elif cell_value == 2:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='gray', outline='black')  # Obstacle
                elif cell_value == 3:
                    self.goal_position = (row, col)
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='green', outline='black')  # Goal
                elif cell_value == 4:
                    self.trail_positions.add((row, col))
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='yellow', outline='black')  # Trail

    def move_robot(self, new_position):
        # Clear the previous robot position and draw the new one
        row, col = new_position
        x1, y1 = col * 100, row * 100
        x2, y2 = x1 + 100, y1 + 100
        self.canvas.create_rectangle(x1, y1, x2, y2, fill='blue', outline='black')

        # Draw the trail if the new position is not an obstacle or goal
        if new_position not in self.trail_positions and new_position != self.goal_position:
            self.trail_positions.add(new_position)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='yellow', outline='black')

        self.canvas.update()


def main():
    # Load map from CSV
    with open('maps/map_01.csv', 'r') as file:
        map_reader = csv.reader(file)
        map_data = [list(map(int, row)) for row in map_reader]

    root = tk.Tk()
    root.title("Robot GUI")

    robot_gui = RobotGUI(root, map_data)

    # Simulate robot movement (replace this with your actual movement logic)
    robot_moves = [(1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4)]

    for move in robot_moves:
        robot_gui.move_robot(move)
        root.update_idletasks()
        root.update()
        root.after(500)  # Adjust the delay (in milliseconds) to control the speed of the visualization

    root.mainloop()


if __name__ == "__main__":
    main()
