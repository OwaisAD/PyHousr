import pandas as pd

# Læs CSV-filen ind i en DataFrame
dataframe = pd.read_csv('house_data_2800.csv')

selected_columns = dataframe[['Adresse', 'Kvadratmeter Pris', 'Byggeår','Energimærke']]

pd.set_option('display.max_rows', None)
print(selected_columns)


