from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import io

from .models import EquipmentDataset
from .serializers import EquipmentDatasetSerializer
from .validators import validate_file_size, validate_file_extension, validate_csv_structure, validate_csv_content


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user_id': user.id, 'username': user.username})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    
    try:
        validate_file_extension(file)
        validate_file_size(file)
    except Exception as e:
        return Response({'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        file.seek(0)
        csv_content = file.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(csv_content))
    except UnicodeDecodeError:
        return Response({'error': 'File encoding must be UTF-8'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'error': 'Failed to parse CSV file'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        validate_csv_structure(df)
        validate_csv_content(df)
    except Exception as e:
        return Response({'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
    
    with transaction.atomic():
        dataset = EquipmentDataset.objects.create(
            filename=file.name,
            total_count=len(df),
            avg_flowrate=round(df['Flowrate'].mean(), 2),
            avg_pressure=round(df['Pressure'].mean(), 2),
            avg_temperature=round(df['Temperature'].mean(), 2),
            type_distribution=df['Type'].value_counts().to_dict(),
            csv_data=csv_content
        )
        
        if EquipmentDataset.objects.count() > 5:
            oldest_ids = list(EquipmentDataset.objects.order_by('uploaded_at', 'id').values_list('id', flat=True)[:EquipmentDataset.objects.count() - 5])
            EquipmentDataset.objects.filter(id__in=oldest_ids).delete()
    
    return Response(EquipmentDatasetSerializer(dataset).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def history(request):
    datasets = EquipmentDataset.objects.order_by('-uploaded_at', '-id')[:5]
    return Response(EquipmentDatasetSerializer(datasets, many=True).data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_dataset_detail(request, pk):
    try:
        dataset = EquipmentDataset.objects.get(pk=pk)
        return Response(EquipmentDatasetSerializer(dataset).data)
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_dataset_visualization(request, pk):
    try:
        dataset = EquipmentDataset.objects.get(pk=pk)
        return Response({
            'type_distribution': {
                'labels': list(dataset.type_distribution.keys()),
                'data': list(dataset.type_distribution.values())
            },
            'averages': {
                'labels': ['Flowrate', 'Pressure', 'Temperature'],
                'data': [dataset.avg_flowrate, dataset.avg_pressure, dataset.avg_temperature]
            }
        })
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def generate_report(request, pk):
    try:
        dataset = EquipmentDataset.objects.get(pk=pk)
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Chemical Equipment Dataset Report", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Dataset ID: {dataset.id}", styles['Normal']))
    elements.append(Paragraph(f"Filename: {dataset.filename}", styles['Normal']))
    elements.append(Paragraph(f"Uploaded At: {dataset.uploaded_at.astimezone().strftime('%Y-%m-%d %I:%M %p')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Summary Statistics", styles['Heading2']))
    elements.append(Paragraph(f"Total Count: {dataset.total_count}", styles['Normal']))
    elements.append(Paragraph(f"Avg Flowrate: {dataset.avg_flowrate}", styles['Normal']))
    elements.append(Paragraph(f"Avg Pressure: {dataset.avg_pressure}", styles['Normal']))
    elements.append(Paragraph(f"Avg Temperature: {dataset.avg_temperature}", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Type Distribution", styles['Heading2']))
    table_data = [['Equipment Type', 'Count']] + [[k, str(v)] for k, v in dataset.type_distribution.items()]
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{dataset.id}.pdf"'
    return response
