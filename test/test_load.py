import pandas as pd
import pytest
from src.data_analysis_pack import join_datasets, load_and_preprocess_population, load_and_preprocess_alcohol, \
    load_and_preprocess_fire_events
from src.data_analysis_pack.io.load import (get_rid_of_double_powiats, alcohol_group_by_powiat,
                                            fire_events_group_by_powiat)


@pytest.fixture
def alcohol_csv(tmp_path):
    import_file = tmp_path / "alcohol.csv"
    data_alco = pd.DataFrame(
        {"Kod pocztowy": ["00-001", "00-002", "00-003", "00-004"],
         "Nazwa firmy": ["Szkoła w Gorlicach", "UW", "PW", "Szkoła w Grodzisku"]})
    data_alco.to_csv(import_file, index=False)
    return import_file


@pytest.fixture
def zipcodes_dict_csv(tmp_path):
    zipcodes_dict = tmp_path / "zipcodes.csv"
    data_dict = pd.DataFrame(
        {"Kod pocztowy": ["00-001", "00-002", "00-003", "00-004"],
         "Powiat": ["Gorlicki", "Warszawa", "Warszawa", "Grodziski"]})
    data_dict.to_csv(zipcodes_dict, index=False)
    return zipcodes_dict


@pytest.fixture
def fire_csv(tmp_path):
    fire_file = tmp_path / "fire_events.csv"
    data = pd.DataFrame(
        {"Powiat": ["Warszawa", "Warszawa", "Gorlicki"], "RAZEM Pożar (P)": [1, 2, 1],
         "RAZEM Miejscowe zagrożenie (MZ)": [0, 1, 0], "RAZEM Alarm fałszywy (AF)": [1, 0, 2],
         "Ilość czerwonych samochodów": [111, 11, 1]})
    data.to_csv(fire_file, index=False)
    return fire_file


@pytest.fixture
def population_xlsx(tmp_path):
    population_file = tmp_path / "population.xlsx"
    pop_data = pd.DataFrame(
        {"Województwa \nVoivodships \nPowiaty \nPowiats": ["Warszawa", "Gorlicki", "aaaaa"],
         "Identyfikator terytorialny\nCode": ["1", "2", pd.NA],
         "Ogółem \nTotal": [100, 102, 0],
         "Mężczyźni Males": [50, 51, 0],
         "Kobiety \nFemales": [50, 51, 0]
         })
    pop_data.to_excel(population_file, index=False, sheet_name="Sheet1", startrow=0)
    return population_file


@pytest.mark.parametrize("data", [pd.DataFrame({"Powiat": ["Grodziski", "Warszawa", "Gorlicki"]})])
def test_get_rid_of_double_powiats(data):
    data = get_rid_of_double_powiats(data)
    assert "grodziski" not in data["Powiat"].str.lower().values
    assert "warszawa" in data["Powiat"].str.lower().values


@pytest.mark.parametrize("data", [pd.DataFrame({"Powiat": ["warszawa", "warszawa", "gorlicki"]})])
def test_alcohol_group_by_powiat(data):
    data = alcohol_group_by_powiat(data)
    assert data.shape == (2, 2)
    data = data[data["Powiat"] == "warszawa"]
    assert len(data) == 1
    assert data["Num of alc"].iloc[0] == 2


@pytest.mark.parametrize("data", [pd.DataFrame({"Powiat": ["warszawa", "warszawa", "gorlicki"],
                                                "RAZEM Pożar (P)": [1, 2, 1],
                                                "RAZEM Miejscowe zagrożenie (MZ)": [0, 1, 0],
                                                "RAZEM Alarm fałszywy (AF)": [1, 0, 2]})])
def test_fire_events_group_by_powiat(data):
    data = fire_events_group_by_powiat(data)
    assert data.shape == (2, 4)
    data = data[data["Powiat"] == "warszawa"]
    assert data["RAZEM Pożar (P)"].iloc[0] == 3


def test_load_and_preprocess_alcohol(alcohol_csv, zipcodes_dict_csv):
    result = load_and_preprocess_alcohol(alcohol_csv, zipcodes_dict_csv)
    assert "Num of alc" in result.columns
    assert "Nazwa firmy" not in result.columns
    assert result.shape == (2, 2)


def test_load_and_preprocess_fire_events(fire_csv):
    result = load_and_preprocess_fire_events(fire_csv)
    assert "RAZEM Pożar (P)" in result.columns
    assert "RAZEM Miejscowe zagrożenie (MZ)" in result.columns
    assert "RAZEM Alarm fałszywy (AF)" in result.columns
    assert "Ilość czerwonych samochodów" not in result.columns
    assert result.shape == (2, 4)


def test_load_and_preprocess_population(population_xlsx):
    result = load_and_preprocess_population(population_xlsx, "Sheet1", 0)
    assert "procentage_of_m" in result.columns
    assert result.shape == (2, 5)
    result = result[result["Powiat"] == "warszawa"]
    assert result["procentage_of_m"].iloc[0] == 50


def test_join_datasets(alcohol_csv, zipcodes_dict_csv, fire_csv, population_xlsx):
    alco_data = load_and_preprocess_alcohol(alcohol_csv, zipcodes_dict_csv)
    fire_data = load_and_preprocess_fire_events(fire_csv)
    population_data = load_and_preprocess_population(population_xlsx, "Sheet1", 0)
    result = join_datasets(alco_data, fire_data, population_data)
    assert result.shape == (2, 8)
    assert result.loc["warszawa", "Num of alc"] == 2
    assert result.loc["warszawa", "RAZEM Pożar (P)"] == 3
    assert result.loc["warszawa", "procentage_of_m"] == 50
