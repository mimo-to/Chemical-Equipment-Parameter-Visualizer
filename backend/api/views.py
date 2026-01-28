from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import pandas as pd
import io
from .models import EquipmentDataset
from .serializers import EquipmentDatasetSerializer

from django.db import transaction

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    
    if not file.name.endswith('.csv'):
        return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)
    
    file.seek(0)
    csv_content = file.read().decode('utf-8')
    
    try:
        df = pd.read_csv(io.StringIO(csv_content))
    except Exception as e:
        return Response({'error': f'CSV parsing failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    
    if df.empty:
        return Response({'error': 'CSV file is empty'}, status=status.HTTP_400_BAD_REQUEST)
    
    required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return Response({'error': f'Missing required columns: {", ".join(missing_columns)}'}, status=status.HTTP_400_BAD_REQUEST)
    
    numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
    
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
        invalid_rows = df[df[col].isna()].index.tolist()
        if invalid_rows:
            return Response({'error': f'Invalid numeric value in column "{col}" at row(s): {invalid_rows}'}, status=status.HTTP_400_BAD_REQUEST)
    
    total_count = len(df)
    avg_flowrate = round(df['Flowrate'].mean(), 2)
    avg_pressure = round(df['Pressure'].mean(), 2)
    avg_temperature = round(df['Temperature'].mean(), 2)
    type_distribution = df['Type'].value_counts().to_dict()
    
    with transaction.atomic():
        dataset = EquipmentDataset.objects.create(
            filename=file.name,
            total_count=total_count,
            avg_flowrate=avg_flowrate,
            avg_pressure=avg_pressure,
            avg_temperature=avg_temperature,
            type_distribution=type_distribution,
            csv_data=csv_content
        )
        
        current_count = EquipmentDataset.objects.count()
        if current_count > 5:
            excess = current_count - 5
            oldest_ids = list(EquipmentDataset.objects.order_by('uploaded_at', 'id').values_list('id', flat=True)[:excess])
            EquipmentDataset.objects.filter(id__in=oldest_ids).delete()
    
    serializer = EquipmentDatasetSerializer(dataset)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def history(request):
    datasets = EquipmentDataset.objects.order_by('-uploaded_at', '-id')[:5]
    serializer = EquipmentDatasetSerializer(datasets, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_dataset_detail(request, pk):
    try:
        dataset = EquipmentDataset.objects.get(pk=pk)
    except EquipmentDataset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = EquipmentDatasetSerializer(dataset)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_dataset_visualization(request, pk):
    try:
        dataset = EquipmentDataset.objects.get(pk=pk)
    except EquipmentDataset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    type_distribution_data = dataset.type_distribution
    labels = list(type_distribution_data.keys())
    data = list(type_distribution_data.values())
    
    response_data = {
        'type_distribution': {
            'labels': labels,
            'data': data
        },
        'averages': {
            'labels': ['Flowrate', 'Pressure', 'Temperature'],
            'data': [dataset.avg_flowrate, dataset.avg_pressure, dataset.avg_temperature]
        }
    }
    return Response(response_data)
