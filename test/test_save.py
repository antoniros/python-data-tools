import pandas as pd
import pytest
from src.data_analysis_pack import save_statistics_as_csv, save_statistics_as_excel


@pytest.fixture
def data():
    return pd.DataFrame({"Kod pocztowy": ["00-001", "00-002", "00-003", "00-004"],
                         "Powiat": ["Gorlicki", "Warszawa", "Warszawa", "Grodziski"]})


def test_save_statistics_as_csv(tmp_path, data):
    result_file = tmp_path / "result.csv"
    save_statistics_as_csv(data, str(result_file), index=False)

    result = pd.read_csv(result_file)
    assert result.equals(data)


def test_save_statistics_as_excel(tmp_path, data):
    result_file = tmp_path / "result.xlsx"
    sheet_name = "Sheet1"
    save_statistics_as_excel(data, str(result_file), sheet_name=sheet_name)
    result = pd.read_excel(result_file, sheet_name=sheet_name, index_col=0)
    assert result.equals(data)


def test_save_statistics_as_csv_invalid_end(data):
    with pytest.raises(AssertionError):
        save_statistics_as_csv(data, "result.txt")


def test_save_statistics_as_excel_invalid_end(data):
    with pytest.raises(AssertionError):
        save_statistics_as_excel(data, "result.txt", sheet_name="Wrong")
