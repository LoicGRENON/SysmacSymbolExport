import copy
import logging
import xml.etree.ElementTree as ET
from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import Dict, List

from sysmac_array import SysmacArray
from sysmac_data_type import SysmacDataType, get_internal_type
from utils import parse_slwd, get_enum_from_namespace, get_struct_from_namespace


logger = logging.getLogger(__name__)


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
            elif s.is_internal_type:
                # TODO
                raise NotImplementedError()
            elif s.is_array:
                array_symbol = SysmacArray(s)
                array_vars = array_symbol.expand()
                if array_symbol.is_base_type:
                    base_type_symbols.extend(array_vars)
                elif array_symbol.is_internal_type:
                    # TODO
                    raise NotImplementedError()
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
            elif s.is_internal_type:
                # TODO
                raise NotImplementedError()
            elif s.is_array:
                array_symbol = SysmacArray(s)
                array_vars = array_symbol.expand()
                if array_symbol.is_base_type:
                    base_type_symbols.extend(array_vars)
                elif array_symbol.is_internal_type:
                    # TODO
                    raise NotImplementedError()
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
                        elif child.is_internal_type:
                            root = ET.fromstring(get_internal_type(child.base_type))
                            new_symbols = [SysmacDataType.import_from_xml(elmt,
                                                                          namespace=child.namespace,
                                                                          parent=new_symbol,
                                                                          prefix=f'{s.name}.{child.name}')
                                           for elmt in root.findall(".//DataType")]
                            user_type_symbols.extend(new_symbols)
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

        data = get_struct_from_namespace(root, namespace)
        data |= get_enum_from_namespace(root, namespace)
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


def get_solutions(solutions_path: str | bytes | PathLike) -> List[SysmacSolution]:
    solutions = [SysmacSolution(solutions_path, s.stem) for s in Path(solutions_path).glob('*/')]
    # Sort the project by last modification date by descending (most recently modified first)
    return sorted(solutions, key=lambda x: x.last_modified, reverse=True)


if __name__ == '__main__':

    from utils import export_symbols_to_file

    logging.basicConfig(level=logging.DEBUG)

    # Production path should be "C:\OMRON\Solution" (or other, depending on the installation directory maybe)
    solutions_path = Path("../assets/Solution")
    solutions = get_solutions(solutions_path)

    # selected_project_uid = '665cc97e-6a2c-4394-a631-1a07a8708a92'
    # selected_project_uid = '2e436523-51e9-41e3-9736-4d6ab40803c1'
    # selected_project_uid = '9e691674-c5bb-45f6-9030-14b61030d1f5'
    # selected_project_uid = 'dcacd5ee-2a81-4251-adb0-8fbbd589108a'
    selected_project_uid = 'e57b7783-9640-42f8-a886-7c1e19aa77fc'

    solution = SysmacSolution(solutions_path, selected_project_uid)
    symbols = solution.get_published_symbols()
    for s in symbols:
        print(f'{s.name} - {s.base_type} - {s.comment}')
    print(f'{len(symbols)} symbols found')

    export_symbols_to_file(symbols, '../assets/symbols.txt')
