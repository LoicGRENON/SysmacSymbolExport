import csv
import os
import sys
import xml.etree.ElementTree as ET
from typing import Dict, List

from sysmac_data_type import SysmacDataType


def export_symbols_to_file(symbols, filename):
    symbols_data = [
        {
            'NAME': s.name,
            'DATATYPE': s.base_type,
            'COMMENT': s.comment,
            'TAGLINK': 'TRUE',
            'RW': 'RW',
        }
        for s in symbols
    ]
    fieldnames = ['HOST', 'NAME', 'DATATYPE', 'ADDRESS', 'COMMENT', 'TAGLINK', 'RW', 'POU']
    # From Weintek documentation, the file should be in ANSI format. Hence, the CP1252 encoding
    with open(filename, 'w', newline='', encoding='cp1252') as f:
        writer = csv.DictWriter(f, delimiter='\t', fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(symbols_data)

def is_pyinstaller_bundle():
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

def get_struct_from_namespace(xml_root: ET.Element, namespace: str):
    data = {}
    for type_def in xml_root.findall(".//DataType[@BaseType='STRUCT']"):
        data_type = SysmacDataType.import_from_xml(type_def, namespace=namespace)
        if data_type.namespace is not None:
            data[f'{data_type.namespace}\\{data_type.name}'] = data_type
        else:
            data[f'{data_type.name}'] = data_type
    return data

def get_enum_from_namespace(xml_root: ET.Element, namespace: str):
    data = {}
    for type_def in xml_root.findall(".//DataType[@BaseType='ENUM']"):
        data_type = SysmacDataType.import_from_xml(type_def, namespace=namespace)
        if data_type.namespace is not None:
            data[f'{data_type.namespace}\\{data_type.name}'] = data_type
        else:
            data[f'{data_type.name}'] = data_type
    return data

def parse_slwd(file_path) -> List[Dict[str, str]]:
    variables = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if not line.startswith("++D="):
                continue  # Skip headers

            # Remove the leading "++D=" and then split by tabs
            line_cleaned = line.strip()[4:]
            parts = line_cleaned.split('\t')

            var_data = {'D': parts[0]}   # The first element is the type (D)
            # The other values follow a key=value pattern
            for part in parts[1:]:
                if "=" in part:
                    key, value = part.split("=", 1)
                    var_data[key] = value
            variables.append(var_data)
    return variables

def resource_path(relative_path):
    """ Get absolute path to resource, mandatory for PyInstaller in one-file mode bundle """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
