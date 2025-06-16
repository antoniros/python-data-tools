import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np


def calculate_statistics(data):
    data = data.select_dtypes(include="number")
    result = pd.DataFrame(
        {"min": data.min(),
         "max": data.max(),
         "mean": data.mean(),
         "median": data.median(),
         "std": data.std(),
         "variance": data.var()
         })
    result = result.round(decimals=3)

    return result


def calculate_correlation(data, col_1, col_2):
    cor, p = np.round(pearsonr(data[col_1], data[col_2]), 3)
    if p >= 0.05:
        result = f"The result is not statistically significant. p-value = {p}."
    elif p >= 0.001:
        result = f"The result is statistically significant. p-value = {p}."
    else:
        result = f"The result is statistically significant. p-value < 0.001."
    return cor, result, p


def plot_correlation(data, col_1, col_2):
    plt.scatter(data[col_1], data[col_2])
    plt.title(f"Correlation between {col_1} and {col_2}")
    plt.xlabel(col_1)
    plt.ylabel(col_2)
    plt.grid(True)
    plt.show()
