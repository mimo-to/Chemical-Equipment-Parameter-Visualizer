from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
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
from datetime import datetime
import pandas as pd
import io

from .models import EquipmentDataset
from .serializers import EquipmentDatasetSerializer
from .validators import validate_file_size, validate_file_extension, validate_csv_structure, validate_csv_content
from .constants import HISTORY_LIMIT
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '')
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user_id': user.id, 'username': user.username})


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    from django.contrib.auth.models import User
    
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '')
    email = request.data.get('email', '').strip()
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if len(password) < 8:
        return Response({'error': 'Password must be at least 8 characters'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password, email=email)
    token = Token.objects.create(user=user)
    return Response({'token': token.key, 'user_id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='user', rate='10/m', block=True)
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
            user=request.user,
            filename=file.name,
            total_count=len(df),
            avg_flowrate=round(df['Flowrate'].mean(), 2),
            avg_pressure=round(df['Pressure'].mean(), 2),
            avg_temperature=round(df['Temperature'].mean(), 2),
            type_distribution=df['Type'].value_counts().to_dict(),
            csv_data=csv_content
        )
        
        user_count = EquipmentDataset.objects.filter(user=request.user).count()
        if user_count > HISTORY_LIMIT:
            oldest_ids = list(EquipmentDataset.objects.filter(user=request.user).order_by('uploaded_at', 'id').values_list('id', flat=True)[:user_count - HISTORY_LIMIT])
            EquipmentDataset.objects.filter(id__in=oldest_ids).delete()
    
    return Response(EquipmentDatasetSerializer(dataset).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def history(request):
    datasets = EquipmentDataset.objects.filter(user=request.user).order_by('-uploaded_at', '-id')[:HISTORY_LIMIT]
    return Response(EquipmentDatasetSerializer(datasets, many=True).data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def compare_datasets(request):
    id1 = request.data.get('dataset1')
    id2 = request.data.get('dataset2')
    
    if not id1 or not id2:
        return Response({'error': 'Both dataset1 and dataset2 IDs required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        ds1 = EquipmentDataset.objects.get(pk=id1, user=request.user)
        ds2 = EquipmentDataset.objects.get(pk=id2, user=request.user)
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found or access denied'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'dataset1': EquipmentDatasetSerializer(ds1).data,
        'dataset2': EquipmentDatasetSerializer(ds2).data,
        'comparison': {
            'flowrate_diff': round(ds1.avg_flowrate - ds2.avg_flowrate, 2),
            'pressure_diff': round(ds1.avg_pressure - ds2.avg_pressure, 2),
            'temperature_diff': round(ds1.avg_temperature - ds2.avg_temperature, 2),
        }
    })


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_dataset_detail(request, pk):
    try:
        dataset = EquipmentDataset.objects.get(pk=pk, user=request.user)
        return Response(EquipmentDatasetSerializer(dataset).data)
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_dataset_visualization(request, pk):
    try:
        dataset = EquipmentDataset.objects.get(pk=pk, user=request.user)
        
        df = pd.read_csv(io.StringIO(dataset.csv_data))
        
        return Response({
            'type_distribution': {
                'labels': list(dataset.type_distribution.keys()),
                'data': list(dataset.type_distribution.values())
            },
            'averages': {
                'labels': ['Flowrate', 'Pressure', 'Temperature'],
                'data': [dataset.avg_flowrate, dataset.avg_pressure, dataset.avg_temperature],
                'min': [float(df['Flowrate'].min()), float(df['Pressure'].min()), float(df['Temperature'].min())],
                'max': [float(df['Flowrate'].max()), float(df['Pressure'].max()), float(df['Temperature'].max())]
            }
        })
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def generate_report(request, pk):
    try:
        dataset = EquipmentDataset.objects.get(pk=pk, user=request.user)
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        df = pd.read_csv(io.StringIO(dataset.csv_data))
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=72, bottomMargin=72)
        styles = getSampleStyleSheet()
        elements = []
        
        elements.append(Paragraph("CHEMICAL EQUIPMENT ANALYSIS REPORT", styles['Title']))
        elements.append(Spacer(1, 12))
        
        meta_data = [
            ['Dataset ID', str(dataset.id)],
            ['Filename', dataset.filename],
            ['Upload Date', dataset.uploaded_at.astimezone().strftime('%Y-%m-%d %I:%M %p')],
            ['Generated', datetime.now().strftime('%Y-%m-%d %I:%M %p')],
            ['Total Records', str(dataset.total_count)]
        ]
        meta_table = Table(meta_data, colWidths=[120, 300])
        meta_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 24))
        
        elements.append(Paragraph("Summary Statistics", styles['Heading2']))
        elements.append(Spacer(1, 8))
        
        stats_data = [
            ['Parameter', 'Mean', 'Min', 'Max'],
            ['Flowrate', f"{dataset.avg_flowrate:.2f}", f"{df['Flowrate'].min():.2f}", f"{df['Flowrate'].max():.2f}"],
            ['Pressure', f"{dataset.avg_pressure:.2f}", f"{df['Pressure'].min():.2f}", f"{df['Pressure'].max():.2f}"],
            ['Temperature', f"{dataset.avg_temperature:.2f}", f"{df['Temperature'].min():.2f}", f"{df['Temperature'].max():.2f}"]
        ]
        stats_table = Table(stats_data, colWidths=[120, 100, 100, 100])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#03045e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#023e8a')),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#caf0f8')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 24))
        
        elements.append(Paragraph("Type Distribution", styles['Heading2']))
        elements.append(Spacer(1, 8))
        
        type_data = [['Equipment Type', 'Count']] + [[k, str(v)] for k, v in dataset.type_distribution.items()]
        type_table = Table(type_data, colWidths=[200, 100])
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#03045e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#023e8a')),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#caf0f8')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(type_table)
        elements.append(Spacer(1, 24))
        
        elements.append(Paragraph("Complete Equipment Data", styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        data_rows = [['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
        for _, row in df.iterrows():
            data_rows.append([
                str(row['Equipment Name']),
                str(row['Type']),
                f"{row['Flowrate']:.2f}",
                f"{row['Pressure']:.2f}",
                f"{row['Temperature']:.2f}"
            ])
        
        data_table = Table(data_rows, colWidths=[90, 90, 80, 80, 90])
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#03045e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#023e8a')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]
        for i in range(1, len(data_rows)):
            bg_color = colors.HexColor('#caf0f8') if i % 2 == 1 else colors.HexColor('#e0f7fa')
            table_style.append(('BACKGROUND', (0, i), (-1, i), bg_color))
        data_table.setStyle(TableStyle(table_style))
        elements.append(data_table)
        
        def add_page_number(canvas, doc):
            canvas.saveState()
            canvas.setFont('Helvetica', 9)
            canvas.setFillColor(colors.HexColor('#03045e'))
            canvas.drawCentredString(letter[0]/2, 30, f"Page {doc.page}")
            canvas.drawString(40, 30, "Chemical Equipment Analysis Report")
            canvas.drawRightString(letter[0]-40, 30, datetime.now().strftime('%Y-%m-%d'))
            canvas.restoreState()
        
        doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{dataset.id}.pdf"'
        return response
    except Exception as e:
        import traceback
        print(f"PDF Generation Error: {str(e)}")
        traceback.print_exc()
        return Response({'error': f'Report generation failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

