import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# TODO
def show_quantum_circuit(figure):
    root = tk.Tk()
    root.title("Quantum Circuit")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    dpi = figure.get_dpi()
    orig_width_in, orig_height_in = figure.get_size_inches()
    orig_width_px = orig_width_in * dpi
    if orig_width_px > screen_width:
        scale_factor = 0.98 * screen_width / orig_width_px
        figure.set_size_inches(
            orig_width_in * scale_factor, orig_height_in * scale_factor, forward=True
        )
    container = tk.Frame(root)
    container.pack(fill="both", expand=True)
    canvas = tk.Canvas(container, bg="white")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    v_scroll = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    h_scroll = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
    h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    inner_frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")
    fig_canvas = FigureCanvasTkAgg(figure, master=inner_frame)
    fig_canvas.draw()
    widget = fig_canvas.get_tk_widget()
    widget.pack(anchor="nw")
    inner_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    root.mainloop()
