import csv

import pandas as pd

signal = pd.read_csv("signal.csv", header=True)
fieldnames = ["sample", "ch1", "ch2"]

with open("data.csv" 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

ptr = 0
while True:
    with open("data.csv", "a") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        samples = {

        }
