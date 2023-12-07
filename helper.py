import numpy as np
import csv


def read_csv(filename: str):
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            data = np.array([list(map(float, row)) for row in reader])
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The specified file: {filename} was not found. {e}")
    except PermissionError as e:
        raise PermissionError(f"Permission error: Unable to open the file {filename}. {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")

    return data
