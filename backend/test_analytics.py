import pandas as pd

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

print('=== Phase 5 Analytics Computation Verification ===\n')
print(f'total_count: {total_count}')
print(f'avg_flowrate: {avg_flowrate}')
print(f'avg_pressure: {avg_pressure}')
print(f'avg_temperature: {avg_temperature}')
print(f'type_distribution: {type_distribution}')
print()

print('=== Validation Checks ===')
print(f'avg_flowrate has 2 decimals: {len(str(avg_flowrate).split(".")[1]) == 2 if "." in str(avg_flowrate) else False}')
print(f'avg_pressure has 2 decimals: {len(str(avg_pressure).split(".")[1]) == 2 if "." in str(avg_pressure) else False}')
print(f'avg_temperature has 2 decimals: {len(str(avg_temperature).split(".")[1]) == 2 if "." in str(avg_temperature) else False}')
print(f'type_distribution sum equals total_count: {sum(type_distribution.values()) == total_count}')
print()

print('=== Test with Different CSV ===')
test_csv_data = '''Equipment Name,Type,Flowrate,Pressure,Temperature
Pump X,Centrifugal,150.5,80.25,70.33
Valve Y,Gate,200.75,90.5,75.67
Tank Z,Storage,100.25,70.75,65.5'''

import io
df2 = pd.read_csv(io.StringIO(test_csv_data))
for col in numeric_columns:
    df2[col] = pd.to_numeric(df2[col], errors='coerce')

total_count2 = len(df2)
avg_flowrate2 = round(df2['Flowrate'].mean(), 2)
avg_pressure2 = round(df2['Pressure'].mean(), 2)
avg_temperature2 = round(df2['Temperature'].mean(), 2)
type_distribution2 = df2['Type'].value_counts().to_dict()

print(f'total_count: {total_count2}')
print(f'avg_flowrate: {avg_flowrate2}')
print(f'avg_pressure: {avg_pressure2}')
print(f'avg_temperature: {avg_temperature2}')
print(f'type_distribution: {type_distribution2}')
print(f'type_distribution sum equals total_count: {sum(type_distribution2.values()) == total_count2}')
