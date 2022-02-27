# import os.path
import time
import serial
import matplotlib
import pandas as pd
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def load_plot(file, canvas):
    signal = pd.read_csv(file, header=None)
    fig = matplotlib.figure.Figure(figsize=(10, 5))
    fig.add_subplot(111).plot(signal[1])
    matplotlib.use("TkAgg")

    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


sg.theme("BrownBlue")
layout = [
    [sg.Text("Signal Logging Options")],
    [
        sg.Text("Device"),
        sg.In(size=(10, 1), enable_events=True, key="-DEVICE-"),
        sg.Text("Baudrate"),
        sg.In(size=(10, 1), enable_events=True, key="-BAUDRATE-"),
        sg.Text("Output File"),
        sg.In(size=(10, 1), enable_events=True, key="-OUTPUT-"),
        sg.Button("Start", size=(10, 1), key="-START-"),
        sg.Button("Stop", size=(10, 1), key="-STOP-"),
        sg.Button("Display", size=(10, 1), key="-DISPLAY-")
    ],
    [sg.Text("Signal")],
    [
        sg.Canvas(key="-CANVAS-")
    ]
]

window = sg.Window("Data Logger", layout, size=(1000, 500))

while True:
    event, values = window.read()
    state = ""
    if event == "Exit" or event == sg.WINDOW_CLOSED:
        break
    elif event == "-START-":
        state = "start"
        with serial.Serial(window["-DEVICE-"].get(), int(window["-BAUDRATE-"].get())) as serialPort, open(window["-OUTPUT-"].get(), 'w') as f:
            now = time.time()
            while state == "start":
                line = serialPort.readline().decode("utf-8", errors="ignore")
                curr_time = time.time() - now
                f.write(f"{curr_time}, {line}")
                f.flush()
    elif event == "-STOP-":
        state = "stop"
    elif event == "-DISPLAY-":
        load_plot(window["-OUTPUT-"].get(), window["-CANVAS-"].TKCanvas)
