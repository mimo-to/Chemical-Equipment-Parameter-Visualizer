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

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from reportlab.lib.validators import Auto

from .models import EquipmentDataset
from .serializers import EquipmentDatasetSerializer
from .validators import validate_file_size, validate_file_extension, validate_csv_structure, validate_csv_content
from .constants import HISTORY_LIMIT
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

@api_view(['GET', 'HEAD'])
@permission_classes([AllowAny])
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
    
    equipment_file = request.FILES['file']
    
    try:
        validate_file_extension(equipment_file)
        validate_file_size(equipment_file)
    except Exception as validation_error:
        return Response({'error': str(validation_error)}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        equipment_file.seek(0)
        file_content = equipment_file.read().decode('utf-8')
        equipment_df = pd.read_csv(io.StringIO(file_content))
    except UnicodeDecodeError:
        return Response({'error': 'File encoding must be UTF-8'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'error': 'Failed to parse CSV file'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        validate_csv_structure(equipment_df)
        validate_csv_content(equipment_df)
    except Exception as structure_error:
        return Response({'error': str(structure_error)}, status=status.HTTP_400_BAD_REQUEST)
    
    with transaction.atomic():
        new_dataset = EquipmentDataset.objects.create(
            user=request.user,
            filename=equipment_file.name,
            total_count=len(equipment_df),
            avg_flowrate=round(equipment_df['Flowrate'].mean(), 2),
            avg_pressure=round(equipment_df['Pressure'].mean(), 2),
            avg_temperature=round(equipment_df['Temperature'].mean(), 2),
            type_distribution=equipment_df['Type'].value_counts().to_dict(),
            csv_data=file_content
        )
        
        current_dataset_count = EquipmentDataset.objects.filter(user=request.user).count()
        if current_dataset_count > HISTORY_LIMIT:
            redundant_dataset_ids = list(EquipmentDataset.objects.filter(user=request.user).order_by('uploaded_at', 'id').values_list('id', flat=True)[:current_dataset_count - HISTORY_LIMIT])
            EquipmentDataset.objects.filter(id__in=redundant_dataset_ids).delete()
    
    return Response(EquipmentDatasetSerializer(new_dataset).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def history(request):
    user_datasets = EquipmentDataset.objects.filter(user=request.user).order_by('-uploaded_at', '-id')[:HISTORY_LIMIT]
    return Response(EquipmentDatasetSerializer(user_datasets, many=True).data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def compare_datasets(request):
    primary_id = request.data.get('dataset1')
    secondary_id = request.data.get('dataset2')
    
    if not primary_id or not secondary_id:
        return Response({'error': 'Both dataset1 and dataset2 IDs required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        primary_dataset = EquipmentDataset.objects.get(pk=primary_id, user=request.user)
        secondary_dataset = EquipmentDataset.objects.get(pk=secondary_id, user=request.user)
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found or access denied'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'dataset1': EquipmentDatasetSerializer(primary_dataset).data,
        'dataset2': EquipmentDatasetSerializer(secondary_dataset).data,
        'comparison': {
            'flowrate_diff': round(primary_dataset.avg_flowrate - secondary_dataset.avg_flowrate, 2),
            'pressure_diff': round(primary_dataset.avg_pressure - secondary_dataset.avg_pressure, 2),
            'temperature_diff': round(primary_dataset.avg_temperature - secondary_dataset.avg_temperature, 2),
        }
    })


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_dataset_detail(request, pk):
    try:
        dataset = EquipmentDataset.objects.get(pk=pk, user=request.user)
        
        return Response({
            'total_count': dataset.total_count,
            'averages': {
                'flowrate': dataset.avg_flowrate,
                'pressure': dataset.avg_pressure,
                'temperature': dataset.avg_temperature
            },
            'type_distribution': dataset.type_distribution
        })
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_dataset_visualization(request, pk):
    try:
        equipment_record = EquipmentDataset.objects.get(pk=pk, user=request.user)
        
        equipment_df = pd.read_csv(io.StringIO(equipment_record.csv_data))
        
        return Response({
            'type_distribution': {
                'labels': list(equipment_record.type_distribution.keys()),
                'data': list(equipment_record.type_distribution.values())
            },
            'averages': {
                'labels': ['Flowrate', 'Pressure', 'Temperature'],
                'data': [equipment_record.avg_flowrate, equipment_record.avg_pressure, equipment_record.avg_temperature],
                'min': [float(equipment_df['Flowrate'].min()), float(equipment_df['Pressure'].min()), float(equipment_df['Temperature'].min())],
                'max': [float(equipment_df['Flowrate'].max()), float(equipment_df['Pressure'].max()), float(equipment_df['Temperature'].max())]
            }
        })
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def generate_report(request, pk):
    try:
        equipment_record = EquipmentDataset.objects.get(pk=pk, user=request.user)
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        equipment_df = pd.read_csv(io.StringIO(equipment_record.csv_data))
        
        report_buffer = io.BytesIO()
        pdf_doc = SimpleDocTemplate(report_buffer, pagesize=letter, topMargin=72, bottomMargin=72)
        pdf_styles = getSampleStyleSheet()
        report_elements = []
        
        report_elements.append(Paragraph("CHEMICAL EQUIPMENT ANALYSIS REPORT", pdf_styles['Title']))
        report_elements.append(Spacer(1, 12))
        
        meta_data = [
            ['Dataset ID', str(equipment_record.id)],
            ['Filename', equipment_record.filename],
            ['Upload Date', equipment_record.uploaded_at.astimezone().strftime('%Y-%m-%d %I:%M %p')],
            ['Generated', datetime.now().strftime('%Y-%m-%d %I:%M %p')],
            ['Total Records', str(equipment_record.total_count)]
        ]
        meta_table = Table(meta_data, colWidths=[120, 300])
        meta_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        report_elements.append(meta_table)
        report_elements.append(Spacer(1, 24))
        
        from reportlab.platypus import KeepTogether
        from reportlab.graphics.charts.barcharts import VerticalBarChart
        from reportlab.graphics.shapes import Drawing
        from reportlab.graphics.charts.textlabels import Label
        
        summary_elements = []
        summary_elements.append(Paragraph("Summary Statistics", pdf_styles['Heading2']))
        summary_elements.append(Spacer(1, 8))
        
        stats_data = [
            ['Parameter', 'Mean', 'Min', 'Max'],
            ['Flowrate', f"{equipment_record.avg_flowrate:.2f}", f"{equipment_df['Flowrate'].min():.2f}", f"{equipment_df['Flowrate'].max():.2f}"],
            ['Pressure', f"{equipment_record.avg_pressure:.2f}", f"{equipment_df['Pressure'].min():.2f}", f"{equipment_df['Pressure'].max():.2f}"],
            ['Temperature', f"{equipment_record.avg_temperature:.2f}", f"{equipment_df['Temperature'].min():.2f}", f"{equipment_df['Temperature'].max():.2f}"]
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
        summary_elements.append(stats_table)
        summary_elements.append(Spacer(1, 12))

        try:
            d_bar = Drawing(400, 200)
            data_averages = [
                float(equipment_record.avg_flowrate),
                float(equipment_record.avg_pressure),
                float(equipment_record.avg_temperature)
            ]
            
            bc = VerticalBarChart()
            bc.x = 50
            bc.y = 50
            bc.height = 125
            bc.width = 300
            bc.data = [data_averages]
            bc.strokeColor = colors.white
            bc.valueAxis.valueMin = 0
            bc.valueAxis.valueMax = max(data_averages) * 1.2
            bc.valueAxis.valueStep = max(data_averages) / 5
            bc.categoryAxis.labels.boxAnchor = 'ne'
            bc.categoryAxis.labels.dx = 8
            bc.categoryAxis.labels.dy = -2
            bc.categoryAxis.labels.angle = 30
            bc.categoryAxis.categoryNames = ['Flowrate', 'Pressure', 'Temp']
            
            bc.bars[0].fillColor = colors.HexColor('#0077b6')
            
            d_bar.add(bc)
            
            lab = Label()
            lab.setOrigin(200, 190)
            lab.boxAnchor = 'ne'
            lab.dx = 0
            lab.dy = 0
            lab.setText('Average Values')
            d_bar.add(lab)

            chart_table_bar = Table([[d_bar]], colWidths=[400])
            chart_table_bar.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            summary_elements.append(chart_table_bar)
        except Exception as e:
            print(f"Bar Chart Error: {e}")
        
        report_elements.append(KeepTogether(summary_elements))
        report_elements.append(Spacer(1, 24))
        
        type_elements = []
        type_elements.append(Paragraph("Type Distribution and Visualization", pdf_styles['Heading2']))
        type_elements.append(Spacer(1, 8))
        
        type_data = [['Equipment Type', 'Count']] + [[k, str(v)] for k, v in equipment_record.type_distribution.items()]
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
        type_elements.append(type_table)
        type_elements.append(Spacer(1, 24))

        if equipment_record.type_distribution:
            try:
                # Increased width to accommodate Legend without overlap
                d = Drawing(500, 250)
                
                pc = Pie()
                pc.x = 50       # Move Pie Left
                pc.y = 50
                pc.width = 150
                pc.height = 150
                
                raw_data = equipment_record.type_distribution
                data = []
                labels = []
                for k, v in raw_data.items():
                    try:
                         val = int(v)
                         data.append(val)
                         labels.append(str(k))
                    except:
                        pass

                if sum(data) > 0:
                    pc.data = data
                    pc.labels = labels
                    pc.simpleLabels = 0 
                    
                    from reportlab.lib import colors as rl_colors
                    chart_colors = [rl_colors.HexColor('#03045e'), rl_colors.HexColor('#0077b6'), 
                                    rl_colors.HexColor('#00b4d8'), rl_colors.HexColor('#90e0ef'),
                                    rl_colors.HexColor('#caf0f8'), rl_colors.HexColor('#fca311'),
                                    rl_colors.HexColor('#e63946')]
                    
                    # Remove stroke to "remove box and colour thing" (cleaner look)
                    pc.slices.strokeWidth = 0
                    for i in range(len(data)):
                        pc.slices[i].fillColor = chart_colors[i % len(chart_colors)]
                    
                    d.add(pc)

                    legend = Legend()
                    legend.alignment = 'right'
                    legend.x = 350          # Move Legend Right
                    legend.y = 100          # Move Legend Down slightly
                    legend.columnMaximum = 10
                    # Ensure Legend text doesn't overlap
                    legend.fontSize = 10
                    legend.dx = 8 
                    legend.dy = 8
                    legend.yGap = 2
                    legend.deltay = 12
                    legend.strokeColor = None  # No border around legend
                    legend.colorNamePairs = [(chart_colors[i % len(chart_colors)], labels[i]) for i in range(len(data))]
                    d.add(legend)
                    
                    # Chart table with increased column width
                    chart_table = Table([[d]], colWidths=[500])
                    chart_table.setStyle(TableStyle([
                        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ]))
                    
                    type_elements.append(chart_table)

                else:
                    type_elements.append(Paragraph("Type Distribution Visualization", pdf_styles['Heading2']))
                    type_elements.append(Spacer(1, 12))
                    type_elements.append(Paragraph("No numeric data available for chart.", pdf_styles['Normal']))
            except Exception as chart_error:
                print(f"Chart Generation Error: {str(chart_error)}")
                type_elements.append(Paragraph(f"Chart Error: {str(chart_error)}", pdf_styles['Italic']))
        else:
             type_elements.append(Paragraph("No distribution data available.", pdf_styles['Normal']))
        
        report_elements.append(KeepTogether(type_elements))
        report_elements.append(Spacer(1, 24))
        
        # Group Complete Data to keep separate or together (User requested one page)
        complete_data_elements = []
        complete_data_elements.append(Paragraph("Complete Equipment Data", pdf_styles['Heading2']))
        complete_data_elements.append(Spacer(1, 12))
        
        data_rows = [['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
        for _, row in equipment_df.iterrows():
            data_rows.append([
                str(row['Equipment Name']),
                str(row['Type']),
                f"{row['Flowrate']:.2f}",
                f"{row['Pressure']:.2f}",
                f"{row['Temperature']:.2f}"
            ])
        
        # Add repeatRows=1 so headers show if it splits across pages
        data_table = Table(data_rows, colWidths=[90, 90, 80, 80, 90], repeatRows=1)
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
        
        complete_data_elements.append(data_table)
        
        # Use KeepTogether to try to force single page, but wrap in try/except or just append
        # For large datasets, KeepTogether might fail or be weird.
        # Given "one page only" request for sample data:
        report_elements.append(KeepTogether(complete_data_elements))
        
        def add_page_number(canvas, doc):
            canvas.saveState()
            canvas.setFont('Helvetica', 9)
            canvas.setFillColor(colors.HexColor('#03045e'))
            canvas.drawCentredString(letter[0]/2, 30, f"Page {doc.page}")
            canvas.drawString(40, 30, "Chemical Equipment Analysis Report")
            canvas.drawRightString(letter[0]-40, 30, datetime.now().strftime('%Y-%m-%d'))
            canvas.restoreState()
        
        pdf_doc.build(report_elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
        report_buffer.seek(0)
        
        response = HttpResponse(report_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{equipment_record.id}.pdf"'
        return response
    except Exception as report_error:
        import traceback
        print(f"PDF Generation Error: {str(report_error)}")
        traceback.print_exc()
        return Response({'error': f'Report generation failed: {str(report_error)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

