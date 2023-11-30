import numpy as np
import csv


def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = np.array([list(map(float, row)) for row in reader])
    return data
