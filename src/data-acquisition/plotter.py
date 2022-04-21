import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


plt.style("fivethirtyeight")


def animate(i):
    signal = pd.read_csv("signal.csv")
    sample = signal("sample")
    channel1 = signal("ch1")
    channel2 = signal("ch2")

    plt.cla()
    plt.plot(sample, channel1, channel2)
    plt.legend(loc="upper left")


ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()
