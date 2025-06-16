import pandas as pd


def save_statistics_as_csv(data, file_path, seperator=',', header=True, index=True):
    assert file_path.endswith('.csv')
    data.to_csv(file_path, sep=seperator, encoding='utf-8', index=index, header=header)


def save_statistics_as_excel(data, file_path, sheet_name):
    assert file_path.endswith('.xlsx')
    data.to_excel(file_path, sheet_name=sheet_name)
