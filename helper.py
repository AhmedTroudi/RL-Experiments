import csv

import numpy as np


def read_csv(filename: str):
    try:
        with open(filename, "r", encoding="UTF-8") as file:
            reader = csv.reader(file)
            data = np.array([list(map(float, row)) for row in reader])
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The specified file: {filename} was not found. {e}"
        ) from e
    except PermissionError as e:
        raise PermissionError(
            f"Permission error: Unable to open the file {filename}. {e}"
        ) from e
    # pylint: disable=broad-exception-raised
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}") from e

    return data
