import pandas as pd
import io

csv_path = '../sample_equipment_data.csv'
df = pd.read_csv(csv_path)

numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

total_count = len(df)
avg_flowrate = round(df['Flowrate'].mean(), 2)
avg_pressure = round(df['Pressure'].mean(), 2)
avg_temperature = round(df['Temperature'].mean(), 2)
type_distribution = df['Type'].value_counts().to_dict()

assert total_count > 0
assert isinstance(avg_flowrate, float)
assert isinstance(avg_pressure, float)
assert isinstance(avg_temperature, float)
assert sum(type_distribution.values()) == total_count

test_csv_data = '''Equipment Name,Type,Flowrate,Pressure,Temperature
Pump X,Centrifugal,150.5,80.25,70.33
Valve Y,Gate,200.75,90.5,75.67
Tank Z,Storage,100.25,70.75,65.5'''

df2 = pd.read_csv(io.StringIO(test_csv_data))
for col in numeric_columns:
    df2[col] = pd.to_numeric(df2[col], errors='coerce')

total_count2 = len(df2)
avg_flowrate2 = round(df2['Flowrate'].mean(), 2)
avg_pressure2 = round(df2['Pressure'].mean(), 2)
avg_temperature2 = round(df2['Temperature'].mean(), 2)
type_distribution2 = df2['Type'].value_counts().to_dict()

assert total_count2 == 3
assert avg_flowrate2 == 150.5
assert avg_pressure2 == 80.5
assert avg_temperature2 == 70.5
assert sum(type_distribution2.values()) == total_count2

print("Analytics verified.")
