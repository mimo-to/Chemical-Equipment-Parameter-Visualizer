from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import pandas as pd
import io
import logging
from .models import EquipmentDataset
from .serializers import EquipmentDatasetSerializer

from django.db import transaction
from django.core.exceptions import ValidationError
from .validators import (
    validate_file_size, 
    validate_file_extension, 
    validate_csv_structure, 
    validate_csv_content
)

logger = logging.getLogger(__name__)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    try:
        if not username or not request.data.get('password'):
            logger.warning(f"Login failed: Missing credentials for username '{username}'")
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=request.data.get('password'))
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            logger.info(f"Login successful: User '{username}'")
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            })
        
        logger.warning(f"Login failed: Invalid credentials for username '{username}'")
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        logger.error(f"Login error for '{username}': {str(e)}", exc_info=True)
        return Response({'error': 'An unexpected error occurred during login'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload(request):
    try:
        user = request.user.username
        if 'file' not in request.FILES:
            logger.error(f"Upload failed: No file provided by user '{user}'")
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        logger.info(f"Upload started: User '{user}', File '{file.name}', Size {file.size} bytes")
        
        try:
            validate_file_extension(file)
        except ValidationError as e:
            logger.warning(f"Upload validation failed (Extension): {str(e.message)}")
            return Response({'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_file_size(file)
        except ValidationError as e:
            logger.warning(f"Upload validation failed (Size): {str(e.message)}")
            return Response({'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            file.seek(0)
            csv_content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            logger.error(f"Upload failed: Encoding error for file '{file.name}'")
            return Response({'error': 'File encoding must be UTF-8'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df = pd.read_csv(io.StringIO(csv_content))
        except Exception:
            logger.error(f"Upload failed: CSV parse error for file '{file.name}'")
            return Response({'error': 'Failed to parse CSV file'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_csv_structure(df)
        except ValidationError as e:
            logger.warning(f"Upload validation failed (Structure): {str(e.message)}")
            return Response({'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_csv_content(df)
        except ValidationError as e:
            logger.warning(f"Upload validation failed (Content): {str(e.message)}")
            return Response({'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_csv_content(df)
        except ValidationError as e:
            logger.warning(f"Upload validation failed (Content): {str(e.message)}")
            return Response({'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        
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
            logger.info(f"Dataset created: ID {dataset.id}, Rows {total_count}")
            
            current_count = EquipmentDataset.objects.count()
            if current_count > 5:
                excess = current_count - 5
                oldest_ids = list(EquipmentDataset.objects.order_by('uploaded_at', 'id').values_list('id', flat=True)[:excess])
                EquipmentDataset.objects.filter(id__in=oldest_ids).delete()
                logger.info(f"Retention policy triggered: Deleted {len(oldest_ids)} old datasets")
        
        serializer = EquipmentDatasetSerializer(dataset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Unexpected upload error: {str(e)}", exc_info=True)
        return Response({'error': 'An unexpected error occurred during upload processing'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def history(request):
    try:
        datasets = EquipmentDataset.objects.order_by('-uploaded_at', '-id')[:5]
        logger.info(f"History accessed by user '{request.user.username}'")
        serializer = EquipmentDatasetSerializer(datasets, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"History fetch error: {str(e)}", exc_info=True)
        return Response({'error': 'Failed to retrieve history'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_dataset_detail(request, pk):
    try:
        dataset = EquipmentDataset.objects.get(pk=pk)
        serializer = EquipmentDatasetSerializer(dataset)
        return Response(serializer.data)
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Dataset detail error: {str(e)}")
        return Response({'error': 'Failed to retrieve dataset details'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from reportlab.pdfgen import canvas
from datetime import datetime
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_dataset_visualization(request, pk):
    try:
        dataset = EquipmentDataset.objects.get(pk=pk)
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
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Visualization error: {str(e)}")
        return Response({'error': 'Failed to generate visualization data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def generate_report(request, pk):
    try:
        dataset = EquipmentDataset.objects.get(pk=pk)
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

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
        data = [['Equipment Type', 'Count']]
        for k, v in dataset.type_distribution.items():
            data.append([k, str(v)])

        t = Table(data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(t)

        doc.build(elements)
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{dataset.id}.pdf"'
        return response
        
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Report generation error: {str(e)}")
        return Response({'error': 'Failed to generate PDF report'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
