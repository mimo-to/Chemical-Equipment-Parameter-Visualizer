import os
import tempfile
from io import StringIO

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

import pandas as pd

from api.validators import (
    validate_file_size,
    validate_file_extension,
    validate_csv_structure,
    validate_csv_content
)
from api.constants import MAX_UPLOAD_SIZE, REQUIRED_COLUMNS


class FileValidatorTests(TestCase):

    def test_file_size_valid(self):
        content = b'a' * 100
        file = SimpleUploadedFile('test.csv', content)
        validate_file_size(file)

    def test_file_size_exceeds_limit(self):
        content = b'a' * (MAX_UPLOAD_SIZE + 1)
        file = SimpleUploadedFile('test.csv', content)
        with self.assertRaises(ValidationError) as ctx:
            validate_file_size(file)
        self.assertIn('limit', str(ctx.exception))

    def test_file_extension_valid_csv(self):
        file = SimpleUploadedFile('data.csv', b'content')
        validate_file_extension(file)

    def test_file_extension_invalid_txt(self):
        file = SimpleUploadedFile('data.txt', b'content')
        with self.assertRaises(ValidationError) as ctx:
            validate_file_extension(file)
        self.assertIn('.csv', str(ctx.exception))

    def test_file_extension_invalid_xlsx(self):
        file = SimpleUploadedFile('data.xlsx', b'content')
        with self.assertRaises(ValidationError) as ctx:
            validate_file_extension(file)
        self.assertIn('.csv', str(ctx.exception))


class CSVStructureTests(TestCase):

    def test_valid_csv_structure(self):
        csv_data = 'Equipment Name,Type,Flowrate,Pressure,Temperature\nPump1,Pump,10,5,25\n'
        df = pd.read_csv(StringIO(csv_data))
        validate_csv_structure(df)

    def test_empty_csv(self):
        df = pd.DataFrame()
        with self.assertRaises(ValidationError) as ctx:
            validate_csv_structure(df)
        self.assertIn('empty', str(ctx.exception).lower())

    def test_missing_required_columns(self):
        csv_data = 'Equipment Name,Type,Flowrate\nPump1,Pump,10\n'
        df = pd.read_csv(StringIO(csv_data))
        with self.assertRaises(ValidationError) as ctx:
            validate_csv_structure(df)
        self.assertIn('Pressure', str(ctx.exception))
        self.assertIn('Temperature', str(ctx.exception))

    def test_extra_columns_rejected(self):
        csv_data = 'Equipment Name,Type,Flowrate,Pressure,Temperature,ExtraCol\nPump1,Pump,10,5,25,X\n'
        df = pd.read_csv(StringIO(csv_data))
        with self.assertRaises(ValidationError) as ctx:
            validate_csv_structure(df)
        self.assertIn('ExtraCol', str(ctx.exception))


class CSVContentTests(TestCase):

    def test_valid_numeric_content(self):
        csv_data = 'Equipment Name,Type,Flowrate,Pressure,Temperature\nPump1,Pump,10.5,5.2,25.0\n'
        df = pd.read_csv(StringIO(csv_data))
        validate_csv_content(df)

    def test_invalid_numeric_value_text(self):
        csv_data = 'Equipment Name,Type,Flowrate,Pressure,Temperature\nPump1,Pump,invalid,5,25\n'
        df = pd.read_csv(StringIO(csv_data))
        with self.assertRaises(ValidationError) as ctx:
            validate_csv_content(df)
        self.assertIn('Flowrate', str(ctx.exception))

    def test_empty_numeric_value(self):
        csv_data = 'Equipment Name,Type,Flowrate,Pressure,Temperature\nPump1,Pump,,5,25\n'
        df = pd.read_csv(StringIO(csv_data))
        with self.assertRaises(ValidationError) as ctx:
            validate_csv_content(df)
        self.assertIn('Flowrate', str(ctx.exception))

    def test_multiple_rows_validates_all(self):
        csv_data = '''Equipment Name,Type,Flowrate,Pressure,Temperature
Pump1,Pump,10,5,25
Valve1,Valve,20,10,30
Heat Exchanger,Exchanger,15,8,50'''
        df = pd.read_csv(StringIO(csv_data))
        validate_csv_content(df)
