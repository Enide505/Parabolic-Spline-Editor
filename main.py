import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline


class SplineEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Редактор параболического сплайна")
        self.geometry("800x650")

        self.points = [(100, 300), (200, 100), (300, 400), (400, 150), (500, 350)]
        self.selected_point = None

        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, 800)
        self.ax.set_ylim(0, 600)
        self.ax.grid(True)
        self.ax.axhline(y=0, color='black', linewidth=1)
        self.ax.axvline(x=0, color='black', linewidth=1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.canvas.mpl_connect("button_release_event", self.on_release)

        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack(fill=tk.X, padx=10, pady=10)

        self.add_point_btn = tk.Button(self.btn_frame, text="Добавить точку", command=self.add_point)
        self.add_point_btn.pack(side=tk.LEFT, padx=5)

        self.remove_point_btn = tk.Button(self.btn_frame, text="Удалить точку", command=self.remove_point)
        self.remove_point_btn.pack(side=tk.LEFT, padx=5)

        self.close_btn = tk.Button(self.btn_frame, text="Закрыть", command=self.close_window)
        self.close_btn.pack(side=tk.RIGHT, padx=5)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.draw_spline()

    def draw_spline(self):
        self.ax.clear()
        self.ax.set_xlim(0, 800)
        self.ax.set_ylim(0, 600)
        self.ax.grid(True)
        self.ax.axhline(y=0, color='black', linewidth=1)
        self.ax.axvline(x=0, color='black', linewidth=1)

        x, y = zip(*self.points)

        if len(self.points) >= 3:
            spline = make_interp_spline(x, y, k=2)
            x_new = np.linspace(min(x), max(x), 500)
            y_new = spline(x_new)
            self.ax.plot(x_new, y_new, 'b-', label='Сплайн')

        self.ax.plot(x, y, 'ro--', label='Ломаная', linestyle='--')

        for i, (px, py) in enumerate(self.points):
            self.ax.text(px, py, f'{i}', fontsize=12, ha='right')

        self.canvas.draw()

    def on_click(self, event):

        if event.inaxes != self.ax:
            return

        for i, (px, py) in enumerate(self.points):
            if abs(px - event.xdata) < 10 and abs(py - event.ydata) < 10:
                self.selected_point = i
                break

    def on_motion(self, event):
        if self.selected_point is None or event.inaxes != self.ax:
            return

        self.points[self.selected_point] = (event.xdata, event.ydata)
        self.draw_spline()

    def on_release(self, event):
        self.selected_point = None

    def add_point(self):
        if len(self.points) >= 2:
            last_x, last_y = self.points[-1]
            new_x = last_x + 50
            new_y = last_y
            self.points.append((new_x, new_y))
            self.draw_spline()

    def remove_point(self):
        if len(self.points) > 3:
            self.points.pop()
            self.draw_spline()

    def close_window(self):
        self.quit()
        self.destroy()


if __name__ == "__main__":
    app = SplineEditor()
    app.mainloop()

