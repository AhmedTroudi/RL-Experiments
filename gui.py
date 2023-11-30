import tkinter as tk


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
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='grey', outline='black')  # Obstacle
                elif cell_value == 3:
                    self.goal_position = (row, col)
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='green', outline='black')  # Goal
                elif cell_value == 4:
                    self.trail_positions.add((row, col))
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='yellow', outline='black')  # Trail
                elif cell_value == 5:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='brown', outline='black')  # Obstacle

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