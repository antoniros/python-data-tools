import pandas as pd
import numpy as np
import pytest
from src.data_analysis_pack import calculate_statistics, calculate_correlation


@pytest.fixture
def data():
    return pd.DataFrame({"population": [1, 2, 3], "Num of alc": [4, 5, 6], "nazwa": ["aaa", "bbb", "ccc"]})


def test_calculate_statistics(data):
    result = calculate_statistics(data)
    assert list(result.columns) == ["min", "max", "mean", "median", "std", "variance"]
    assert np.isclose(result.loc["Num of alc", "mean"], 5)
    assert np.isclose(result.loc["population", "min"], 1)
    assert np.isclose(result.loc["population", "variance"], 1, np.var(data["population"], ddof=1))
    assert "nazwa" not in result.index
    assert "population" in result.index and "Num of alc" in result.index
    assert result.shape == (2, 6)


def test_calculate_correlation_correct(data):
    assert np.isclose(calculate_correlation(data, "population", "Num of alc")[0], 1)
