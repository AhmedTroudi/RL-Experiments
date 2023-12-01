import numpy as np
import csv


def read_csv(filename: str):
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            data = np.array([list(map(float, row)) for row in reader])
    except FileNotFoundError:
        print(f"The specified file: {filename} was not found.")
    except PermissionError:
        print(f"Permission error: Unable to open the file {filename}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return data
