import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import EquipmentDataset

print('=== Database Records Verification ===\n')

datasets = EquipmentDataset.objects.all().order_by('id')
print(f'Total records in database: {datasets.count()}\n')

for dataset in datasets:
    print(f'Record ID: {dataset.id}')
    print(f'Filename: {dataset.filename}')
    print(f'Uploaded at: {dataset.uploaded_at}')
    print(f'Total count: {dataset.total_count}')
    print(f'Avg flowrate: {dataset.avg_flowrate}')
    print(f'Avg pressure: {dataset.avg_pressure}')
    print(f'Avg temperature: {dataset.avg_temperature}')
    print(f'Type distribution: {dataset.type_distribution}')
    print(f'CSV data length: {len(dataset.csv_data)} characters')
    print()
