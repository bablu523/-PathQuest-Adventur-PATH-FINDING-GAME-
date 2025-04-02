import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from algorithms import a_star, dijkstra, bfs
import time

class PathfindingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("PathQuest Adventure")
        self.root.geometry("800x650")

        self.create_map_grid()
        self.create_controls()

        self.start = None
        self.end = None
        self.obstacles = set()
        self.algorithm = "A*"

        # Load images for character, treasure, obstacles
        self.start_img = ImageTk.PhotoImage(Image.open("images/character.png").resize((30, 30)))
        self.end_img = ImageTk.PhotoImage(Image.open("images/treasure.png").resize((30, 30)))
        self.obstacle_img = ImageTk.PhotoImage(Image.open("images/rock.png").resize((30, 30)))

    def create_map_grid(self):
        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="tan")
        self.canvas.grid(row=0, column=0)

        self.grid_size = 20
        self.cell_size = 30
        self.cells = {}

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell = self.canvas.create_rectangle(
                    col * self.cell_size, row * self.cell_size,
                    (col + 1) * self.cell_size, (row + 1) * self.cell_size,
                    outline="gray", fill="green"
                )
                self.cells[(row, col)] = cell

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def create_controls(self):
        frame = tk.Frame(self.root)
        frame.grid(row=0, column=1, padx=20)

        self.algorithm_var = tk.StringVar(value="A*")
        algorithm_menu = tk.OptionMenu(frame, self.algorithm_var, "A*", "Dijkstra", "BFS")
        algorithm_menu.grid(row=0, column=0, pady=10)

        start_button = tk.Button(frame, text="Start Adventure", command=self.start_pathfinding)
        start_button.grid(row=1, column=0, pady=10)

        reset_button = tk.Button(frame, text="Reset Map", command=self.reset_map)
        reset_button.grid(row=2, column=0, pady=10)

        clear_button = tk.Button(frame, text="Clear Path", command=self.clear_path)
        clear_button.grid(row=3, column=0, pady=10)

    def on_canvas_click(self, event):
        row = event.y // self.cell_size
        col = event.x // self.cell_size

        if (row, col) not in self.cells:
            return

        if self.start is None:
            self.start = (row, col)
            self.canvas.create_image(col * self.cell_size + 15, row * self.cell_size + 15, image=self.start_img)
        elif self.end is None:
            self.end = (row, col)
            self.canvas.create_image(col * self.cell_size + 15, row * self.cell_size + 15, image=self.end_img)
        else:
            if (row, col) not in self.obstacles:
                self.obstacles.add((row, col))
                self.canvas.create_image(col * self.cell_size + 15, row * self.cell_size + 15, image=self.obstacle_img)

    def start_pathfinding(self):
        if not self.start or not self.end:
            messagebox.showerror("Error", "Please set both start and end points.")
            return

        self.clear_path()

        algorithm = self.algorithm_var.get()
        if algorithm == "A*":
            path = a_star(self.start, self.end, self.obstacles, self.grid_size)
        elif algorithm == "Dijkstra":
            path = dijkstra(self.start, self.end, self.obstacles, self.grid_size)
        elif algorithm == "BFS":
            path = bfs(self.start, self.end, self.obstacles, self.grid_size)

        if path:
            for (row, col) in path:
                cell = self.cells[(row, col)]
                self.canvas.itemconfig(cell, fill="yellow")
                self.root.update()
                time.sleep(0.05)
        else:
            messagebox.showerror("Error", "No path found.")

    def clear_path(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if (row, col) not in [self.start, self.end] and (row, col) not in self.obstacles:
                    self.canvas.itemconfig(self.cells[(row, col)], fill="green")

    def reset_map(self):
        self.start = None
        self.end = None
        self.obstacles.clear()

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.canvas.itemconfig(self.cells[(row, col)], fill="green")

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingGame(root)
    root.mainloop()
