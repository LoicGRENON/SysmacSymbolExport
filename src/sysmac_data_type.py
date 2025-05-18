
BASE_TYPES = [
    'BOOL',
    'BYTE',
    'DATE',
    'DATE_AND_TIME',
    'DINT',
    'DWORD',
    'INT',
    'LINT',
    'LREAL',
    'LWORD',
    'REAL',
    'SINT',
    'STRING',
    'TIME',
    'TIME_OF_DAY',
    'UDINT',
    'UINT',
    'ULINT',
    'USINT',
    'WORD'
]


class SysmacDataType:

    def __init__(self):
        self.namespace = None
        self.parent = None
        self.defined = False
        self.children = None
        self.network_publish = None

        self.name = None
        self.base_type = None
        self.array_type = None
        self.length = None
        self.initial_value = None
        self.enum_value = None
        self.comment = None
        self.offset_channel = None
        self.offset_bit = None
        self.is_controller_defined_type = None
        self.order = None
        self.offset_type = None

    def __repr__(self):
        if self.parent is not None:
            return f'{repr(self.parent)[:-1]}\\{self.name})'
        else:
            if self.namespace is not None:
                return f'{self.__class__.__name__}({self.namespace}\\{self.name})'
            else:
                return f'{self.__class__.__name__}({self.name})'

    def _parse_xml(self, xml_element, namespace=None, parent=None):
        self.namespace = namespace
        self.parent = parent
        self.name = xml_element.get('Name')
        self.base_type = xml_element.get('BaseType')
        self.array_type = xml_element.get('ArrayType')
        self.length = xml_element.get('Length')
        self.initial_value = xml_element.get('InitialValue')
        self.enum_value = xml_element.get('EnumValue')
        self.comment = xml_element.get('Comment')
        self.offset_channel = xml_element.get('OffsetChannel')
        self.offset_bit = xml_element.get('OffsetBit')
        self.is_controller_defined_type = xml_element.get('IsControllerDefinedType')
        self.order = xml_element.get('Order')
        self.offset_type = xml_element.get('OffsetType')
        return self

    def _parse_slwd(self, slwd_dict, namespace=None, parent=None):
        self.namespace = namespace
        self.parent = parent
        self.name = slwd_dict['N']
        self.base_type = slwd_dict['D']
        self.network_publish = slwd_dict.get('NTP')
        self.array_type = None
        self.length = None
        self.initial_value = slwd_dict.get('IV')
        self.enum_value = None  # TODO: Vérifier la déclaration d'un type Enum dans les variables globales
        self.comment = slwd_dict.get('Com')
        self.offset_channel = None
        self.offset_bit = None
        self.is_controller_defined_type = False
        self.order = None
        self.offset_type = None
        return self

    @classmethod
    def import_from_xml(cls, xml_element, namespace=None, parent=None):
        return cls()._parse_xml(xml_element, namespace=namespace, parent=parent)

    @classmethod
    def import_from_slwd(cls, slwd_dict, namespace=None, parent=None):
        return cls()._parse_slwd(slwd_dict, namespace=namespace, parent=parent)

    @property
    def is_base_type(self):
        return self.base_type in BASE_TYPES

    @property
    def is_array(self):
        return self.base_type.startswith('ARRAY')

    @property
    def is_struct(self):
        return self.base_type == 'STRUCT'

    @property
    def is_enum(self):
        return self.base_type == 'ENUM'
