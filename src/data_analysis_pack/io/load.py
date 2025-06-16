import pandas as pd


def get_rid_of_double_powiats(data):
    double_powiats = ["bielski", "brzeski", "grodziski", "krośnieński", "nowodworski",
                      "opolski", "ostrowski", "średzki", "świdnicki", "tomaszowski"]

    data["Powiat"] = data["Powiat"].str.strip().str.lower()
    data = data[~data["Powiat"].isin(double_powiats)].reset_index(drop=True)
    return data


def load_and_preprocess_alcohol(import_file, zipcodes_dict):
    # doesn't contain powiat as one of columns, we need a dictionary with zipcodes
    # 31 of 416 company zipcodes didn't appear in the dictionary: we lost around 7.5% of data
    data = pd.read_csv(import_file)
    dictionary = pd.read_csv(zipcodes_dict)
    result = pd.merge(data, dictionary, how="left", on="Kod pocztowy")
    result = result.dropna(subset=["Powiat"])
    result = result.reset_index(drop=True)
    result = alcohol_group_by_powiat(result)
    result = get_rid_of_double_powiats(result)
    return result


def alcohol_group_by_powiat(data):
    data = data.groupby(by="Powiat").size().reset_index(name="Num of alc")
    return data


def load_and_preprocess_fire_events(import_file):
    data = pd.read_csv(import_file)
    data = data[["Powiat", "RAZEM Pożar (P)", "RAZEM Miejscowe zagrożenie (MZ)", 'RAZEM Alarm fałszywy (AF)']]
    data = fire_events_group_by_powiat(data)
    data = get_rid_of_double_powiats(data)
    return data


def fire_events_group_by_powiat(data):
    data = data.groupby(by="Powiat").sum()
    data.reset_index(inplace=True)
    return data


def load_and_preprocess_population(import_file, name_of_sheet, rows_to_skip, index_column=None):
    # already grouped by powiat, cleaning empty rows from Excel
    # results in 380 rows, which is the number of powiats in Poland
    # but there are 10 pairs of powiats with the same name,
    # it's possible to differenciate them, but it's honestly a bit too hard
    # so I will just get rid of all 20 of them
    data = pd.read_excel(import_file, sheet_name=name_of_sheet, skiprows=rows_to_skip, index_col=index_column)
    data = data[['Województwa \nVoivodships \nPowiaty \nPowiats', 'Identyfikator terytorialny\nCode', 'Ogółem \nTotal',
                 'Mężczyźni Males', 'Kobiety \nFemales']]
    data.columns = ["Powiat", "id", "num", "m", "f"]
    data = data.dropna(subset=['id'])
    data = data.reset_index(drop=True)
    data = data[["Powiat", "num", "m", "f"]]
    data["procentage_of_m"] = data["m"] / (data["m"] + data["f"]) * 100
    data = get_rid_of_double_powiats(data)
    data["Powiat"] = data["Powiat"].replace("m. st. warszawa", "warszawa")
    return data


def join_datasets(alco_data, fire_events_data, population_data):
    # only population has all powiats (as not every powiat had an alcohol company or a fire event)
    # during the merge I'll fill the missing values with zeros as there were no companies or events
    # additionaly population data has Warsaw saved as M. St. Warszawa instead of Warszawa
    result = pd.merge(population_data, alco_data, on='Powiat', how='left')
    result = pd.merge(result, fire_events_data, on='Powiat', how='left')
    result[['Num of alc', 'RAZEM Pożar (P)', 'RAZEM Miejscowe zagrożenie (MZ)', 'RAZEM Alarm fałszywy (AF)']] = (
        result[['Num of alc', 'RAZEM Pożar (P)', 'RAZEM Miejscowe zagrożenie (MZ)', 'RAZEM Alarm fałszywy (AF)']].fillna(0))
    result.set_index("Powiat", inplace=True)
    return result
