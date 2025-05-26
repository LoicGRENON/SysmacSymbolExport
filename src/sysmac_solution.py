import copy
import logging
import xml.etree.ElementTree as ET
from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import Dict, List

from sysmac_array import SysmacArray
from sysmac_data_type import SysmacDataType


logger = logging.getLogger(__name__)


def get_solutions(solutions_path: str | bytes | PathLike) -> List['SysmacSolution']:
    solutions = [SysmacSolution(solutions_path, s.stem) for s in Path(solutions_path).glob('*/')]
    # Sort the project by last modification date by descending (most recently modified first)
    return sorted(solutions, key=lambda x: x.last_modified, reverse=True)

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

def _get_struct_from_namespace(xml_root: ET.Element, namespace: str):
    data = {}
    for type_def in xml_root.findall(".//DataType[@BaseType='STRUCT']"):
        data_type = SysmacDataType.import_from_xml(type_def, namespace=namespace)
        if data_type.namespace is not None:
            data[f'{data_type.namespace}\\{data_type.name}'] = data_type
        else:
            data[f'{data_type.name}'] = data_type
    return data

def _get_enum_from_namespace(xml_root: ET.Element, namespace: str):
    data = {}
    for type_def in xml_root.findall(".//DataType[@BaseType='ENUM']"):
        data_type = SysmacDataType.import_from_xml(type_def, namespace=namespace)
        if data_type.namespace is not None:
            data[f'{data_type.namespace}\\{data_type.name}'] = data_type
        else:
            data[f'{data_type.name}'] = data_type
    return data


class SysmacSolution:
    def __init__(self, solutions_path, uuid):
        self.solutions_path = Path(solutions_path)
        self._uuid = uuid
        self._name = ''
        self._author = ''
        self._project_type = ''
        self._last_modified = datetime.fromtimestamp(0)
        self.global_vars = []

        self._get_properties()

    @property
    def author(self):
        return self._author

    @property
    def last_modified(self):
        return self._last_modified

    @property
    def name(self):
        return self._name

    @property
    def project_type(self):
        return self._project_type

    @property
    def uuid(self):
        return self._uuid

    def get_global_vars(self) -> List[SysmacDataType]:
        project_oem_file = f'{self._uuid}.oem'
        tree = ET.parse(self.solutions_path / self._uuid / project_oem_file)
        root = tree.getroot()
        global_vars_filename = root.find(".//Entity[@type='Variables'][@subtype='Global']").attrib.get('id')
        self.global_vars = [SysmacDataType.import_from_slwd(symbol)
                            for symbol in parse_slwd(self.solutions_path / self._uuid / f"{global_vars_filename}.xml")]
        return self.global_vars

    def get_published_symbols(self) -> List[SysmacDataType]:
        base_type_symbols = []
        user_type_symbols = []

        dt = self._get_data_types()
        self.get_global_vars()

        # Go through the global variables and expand STRUCT type symbols
        # When the symbols are from base type, they are added to base_type_symbols list
        # Custom type symbols are added to user_type_symbols list to be expanded later on.
        for s in self.global_vars:
            if not s.network_publish or s.network_publish != 'PublicationOnly':
                continue

            if s.is_base_type:
                base_type_symbols.append(s)
            elif s.is_array:
                array_symbol = SysmacArray(s)
                array_vars = array_symbol.expand()
                if array_symbol.is_base_type:
                    base_type_symbols.extend(array_vars)
                else:
                    user_type_symbols.extend(array_vars)
            # TODO: Check what happens for a global variable derived from type ENUM
            # elif dt[s.base_type].is_enum:
            #     s.base_type = 'DINT'
            #     base_type_symbols.append(s)
            elif s.base_type in dt.keys():
                user_type_symbols.append(s)
            else:
                logger.info(f'"{s.name}" symbol of type <{s.base_type}> has been skipped !!)')

        # Custom type symbols are added to user_type_symbols list
        # Go through that list to expand the variables till getting the members from base type.
        while len(user_type_symbols) > 0:
            s = user_type_symbols.pop()
            if s.is_base_type:
                base_type_symbols.append(s)
                continue
            elif s.is_array:
                array_symbol = SysmacArray(s)
                array_vars = array_symbol.expand()
                if array_symbol.is_base_type:
                    base_type_symbols.extend(array_vars)
                else:
                    user_type_symbols.extend(array_vars)
                continue
            elif s.base_type in dt.keys():
                if dt[s.base_type].is_enum:
                    s.base_type = 'DINT'
                    base_type_symbols.append(s)
                    continue
                elif dt[s.base_type].is_struct:
                    for child in dt[s.base_type].children:
                        new_symbol = copy.deepcopy(child)
                        new_symbol.parent = None
                        new_symbol.namespace = None
                        new_symbol.name = f'{s.name}.{child.name}'
                        if child.is_base_type:
                            base_type_symbols.append(new_symbol)
                        else:
                            user_type_symbols.append(new_symbol)
            else:
                logger.info(f'"{s.name}" symbol of type <{s.base_type}> has been skipped !!)')

        base_type_symbols.sort(key=lambda x: x.name)
        return base_type_symbols

    def _get_data_types(self) -> Dict[str, SysmacDataType]:
        project_oem_file = f'{self._uuid}.oem'
        tree = ET.parse(self.solutions_path / self._uuid / project_oem_file)
        root = tree.getroot()

        dt = {}
        for entity in root.iter('Entity'):
            if entity.get('type') == 'Group' and entity.get('subtype') == 'IecData':
                for child in entity.find('ChildEntities'):
                    if child.tag == 'Entity' and child.get('type') == 'DataType':
                        # Extend the dictionary with new values
                        dt |= self._get_data_from_namespace(child.get('id'), child.get('namespace'))

        return dt

    def _get_data_from_namespace(self, datatype_id, namespace=None) -> Dict[str, SysmacDataType]:
        datatype_file = f"{datatype_id}.xml"
        tree = ET.parse(self.solutions_path / self._uuid / datatype_file)
        root = tree.getroot()

        data = _get_struct_from_namespace(root, namespace)
        data |= _get_enum_from_namespace(root, namespace)
        return data

    def _get_properties(self):
        try:
            tree = ET.parse(self.solutions_path / self._uuid / f'{self._uuid}.xml')
        except FileNotFoundError as e:
            return
        root = tree.getroot()

        self._project_type = root.find('.//ProjectType').text
        self._author = root.find('.//Author').text
        self._last_modified = datetime.fromisoformat(root.find('.//DateModified').text)

        tree = ET.parse(self.solutions_path / self._uuid / f'{self._uuid}.oem')
        root = tree.getroot()
        solution_element = root.find(".//Entity[@type='Solution']")
        self._name = solution_element.attrib.get('name') if solution_element is not None else ''
