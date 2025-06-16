import pandas as pd
import tabula

top_mm = 10
bottom_mm = 10
page_height = 297
top = top_mm * 2.83465
bottom = (page_height - bottom_mm) * 2.83465
left = 0
right = 210 * 2.83465

tables = tabula.read_pdf("PNA.pdf", pages="4-1648", area=(top, left, bottom, right), multiple_tables=True, stream=True)

data = pd.concat(tables)[["PNA", "Powiat", "Gmina"]]
data.columns = ["Kod pocztowy", "Powiat", "Gmina"]
data = data.dropna(subset=["Kod pocztowy", "Powiat", "Gmina"], how="any")
data = data.drop_duplicates(subset=["Kod pocztowy"])
data.to_csv("../data/alcohol_data/zipcodes_dict.csv", index=False)
