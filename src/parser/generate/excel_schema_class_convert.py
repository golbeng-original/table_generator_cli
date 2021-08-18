from typing import overload
from openpyxl.reader import excel

from parser.schema_table_parser import ExcelSchemaData, ExcelSchemaField
from generate.generate_struct import ConvertTargetType

_MAPPING_TYPE = {
    ConvertTargetType.CSharp : {
        'string' : 'string',
        'int' : 'int',
        'uint' : 'uint',
        'float' : 'float',
        'bool' : 'bool'
    },
    ConvertTargetType.Dart : {
        'string' : 'String',
        'int' : 'int',
        'uint' : 'int',
        'float' : 'double',
        'bool' : 'bool'
    }
}

_MAPPING_DEFAULT_CONTEXT = {
    ConvertTargetType.CSharp : {
        'string' : lambda default : '"{0}"'.format(default),
        'int' : lambda default : '0' if len(default) == 0 else default,
        'uint' : lambda default : '0' if len(default) == 0 else default,
        'float' : lambda default : '0.0f' if len(default) == 0 else default,
        'bool' : lambda default : 'false' if len(default) == 0 else default.lower(),
    },
    ConvertTargetType.Dart : {
        'string' : lambda default : '\'{0}\''.format(default),
        'int' : lambda default : '0' if len(default) == 0 else default,
        'uint' : lambda default : '0' if len(default) == 0 else default,
        'float' : lambda default : '0.0' if len(default) == 0 else default,
        'bool' : lambda default : 'false' if len(default) == 0 else default.lower(),
    }
}

_MAPPING_ENUM_DEFAULT_CONTEXT = {
    ConvertTargetType.CSharp : lambda type, default : '' if len(default) == 0 else '.'.join([type, default]),
    ConvertTargetType.Dart : lambda type, default : '' if len(default) == 0 else '.'.join([type, default.lower()]),
}

class ConvertedSchemaField:
    '''
    ExcelSchmeaField로 부터 생성되는 class generate 용 field
    - 'primary', 'secondary' 는 데이터 조회의 기본키
    - is_primary : field name이 'primary key'이면.. True
    - is_secondary : field name이 'secondary key'이면.. True
    '''

    type_str:str = ''
    field_name:str = ''
    default_context:str = ''
    is_primary:bool = False
    is_secondary:bool = False

    def __init__(self, excel_schema_field:ExcelSchemaField, convert_target_type:ConvertTargetType):
        self.field_name = excel_schema_field.name
        
        if excel_schema_field.name.lower() == 'primarykey':
            self.is_primary = True

        if excel_schema_field.name.lower() == 'secondarykey':
            self.is_secondary = True

        field_type = excel_schema_field.type.lower()
        default = excel_schema_field.default
        if field_type == 'string':
            self.type_str = self.__get_type_str(convert_target_type, field_type)
            self.default_context = self.__get_type_default_context(convert_target_type, field_type, default)

        elif field_type == 'int':
            self.type_str = self.__get_type_str(convert_target_type, field_type)
            self.default_context = self.__get_type_default_context(convert_target_type, field_type, default)

        elif field_type == 'uint':
            self.type_str = self.__get_type_str(convert_target_type, field_type)
            self.default_context = self.__get_type_default_context(convert_target_type, field_type, default)

        elif field_type == 'float':
            self.type_str = self.__get_type_str(convert_target_type, field_type)
            self.default_context = self.__get_type_default_context(convert_target_type, field_type, default)

        elif field_type == 'bool':
            self.type_str = self.__get_type_str(convert_target_type, field_type)
            self.default_context = self.__get_type_default_context(convert_target_type, field_type, default)

        else:
            self.type_str = excel_schema_field.type
            self.default_context = self.__get_enum_type_default_context(convert_target_type, excel_schema_field.type, default)

    def __get_type_str(self, convert_target_type: ConvertTargetType, type:str):

        if convert_target_type not in _MAPPING_TYPE:
            raise Exception('{0} is not define in __MAPPING_TYPE'.format(convert_target_type))

        target_mapping = _MAPPING_TYPE[convert_target_type]

        if type not in target_mapping:
            raise Exception('{0} - {1} type not define in __MAPPING_TYPE'.format(convert_target_type, type)) 

        return target_mapping[type]

    def __get_type_default_context(self, convert_target_type: ConvertTargetType, type:str, default:str):

        if convert_target_type not in _MAPPING_DEFAULT_CONTEXT:
            raise Exception('{0} is not define in __MAPPING_TYPE'.format(convert_target_type))

        target_mapping = _MAPPING_DEFAULT_CONTEXT[convert_target_type]

        if type not in target_mapping:
            raise Exception('{0} - {1} type not define in __MAPPING_TYPE'.format(convert_target_type, type)) 

        return target_mapping[type](default=default)

    def __get_enum_type_default_context(self, convert_target_type: ConvertTargetType, type:str, default:str):
        if convert_target_type not in _MAPPING_ENUM_DEFAULT_CONTEXT:
            raise Exception('{0} is not define in _MAPPING_ENUM_DEFAULT_CONTEXT'.format(convert_target_type))

        defult_context_func = _MAPPING_ENUM_DEFAULT_CONTEXT[convert_target_type]
        return defult_context_func(type, default)

    def is_pk_field(self):
        return self.is_primary == True or self.is_secondary == True


class SchemaClassConverter:

    _convert_target_type:ConvertTargetType = ConvertTargetType.Empty
    _excel_schema_data:ExcelSchemaData = None
    _db_extension:str = ''

    def __init__(self, excel_schema_data:ExcelSchemaData, db_extension:str):
        self._excel_schema_data = excel_schema_data
        self._db_extension = db_extension

    def get_converted_fields(self):
        for schmea_field in self._excel_schema_data.get_fields():
            yield ConvertedSchemaField(schmea_field, self._convert_target_type)

    def generate(self):
        return ''

    def generate_meta(self):
        return ''


class CSharpSchemaClassConverter(SchemaClassConverter):

    def __init__(self, excel_schema_data:ExcelSchemaData, db_extension:str):
        super().__init__(excel_schema_data, db_extension)
        self._convert_target_type = ConvertTargetType.CSharp

    # override
    def generate(self):
        return self.__generate_class_unit()

    def generate_meta(self, meta_mapping_variable:str = 'TableMetaMapping'):
        prefix = ''
        
        builder = ''
        builder += prefix + '{0}.Add(typeof({1}), new TableMeta()\n'.format(meta_mapping_variable, self._excel_schema_data.table_name)
        builder += prefix + '{\n'
        builder += prefix + '\ttableName = "{0}",\n'.format(self._excel_schema_data.table_name)
        builder += prefix + '\tdbName = "{0}{1}",\n'.format(self._excel_schema_data.db_name, self._db_extension)
        builder += prefix + '});\n'

        return builder

    def __generate_class_unit(self):

        table_name = self._excel_schema_data.table_name

        class_builder = ''
        class_builder += 'public class {0} : TblBase\n'.format(table_name)
        class_builder += '{\n'

        # Property Generate
        converted_fields = list(self.get_converted_fields())
        for converted_field in converted_fields:

            if converted_field.is_pk_field() == True:
                class_builder += self.__generate_pk_key_field(converted_field)
            
            else:
                class_builder += self.__generate_none_pk_key_field(converted_field)

        # Property Meta
        class_builder += '\n'
        class_builder += '\tpublic override int propertiesCount {{ get => {0}; }}\n'.format(self._excel_schema_data.get_field_count())

        class_builder += '\n'
        class_builder += self.__generate_get_property_func(converted_fields)

        class_builder += '\n'
        class_builder += self.__generate_set_property_func(converted_fields)

        class_builder += '}\n'

        return class_builder

    def __generate_pk_key_field(self, converted_field:ConvertedSchemaField):

        default_context = converted_field.default_context
        if len(default_context):
            default_context = '= {0}'.format(default_context)

        private_field_name = '_{0}'.format(converted_field.field_name)
        is_primary_key_str = 'true' if converted_field.is_primary else 'false'

        field_builder = ''
        field_builder += '\tprivate {0} {1}{2};\n'.format(converted_field.type_str, private_field_name, default_context)
        field_builder += '\tpublic  {0} {1}\n'.format(converted_field.type_str, converted_field.field_name)
        field_builder += '\t{\n'
        field_builder += '\t\tget => {0};\n'.format(private_field_name)
        field_builder += '\t\tset\n'
        field_builder += '\t\t{\n'
        field_builder += '\t\t\t{0} = value;\n'.format(private_field_name)
        field_builder += '\t\t\tConvertKey({0}, {1});\n'.format(private_field_name, is_primary_key_str)
        field_builder += '\t\t}\n'
        field_builder += '\t}\n'

        return field_builder

    def __generate_none_pk_key_field(self, converted_field:ConvertedSchemaField):
        
        default_context = converted_field.default_context
        if len(default_context) > 0:
            default_context = '= {0};'.format(default_context)

        accessor_str = '{ get; set; }'

        field_builder = '\tpublic {0} {1} {2} {3}\n'.format(converted_field.type_str, converted_field.field_name, accessor_str, default_context)
        return field_builder

    def __generate_get_property_func(self, converted_fields:list):
        func_builder = ''
        func_builder += '\tpublic override (string propertyName, Type type)? GetPropertyInfo(int index)\n'
        func_builder += '\t{\n'

        func_builder += '\t\tswitch (index)\n'
        func_builder += '\t\t{\n'

        for idx, converted_field in enumerate(converted_fields):
            func_builder += '\t\t\tcase {0}: return (nameof({1}), {1}.GetType());\n'.format(idx, converted_field.field_name)

        func_builder += '\t\t}\n'

        func_builder += '\t\treturn null;\n' 
        func_builder += '\t}\n'

        return func_builder

    def __generate_set_property_func(self, converted_fields:list):
        func_builder = ''
        func_builder += '\tpublic override bool SetPropertyValue(string propertyName, object value)\n'
        func_builder += '\t{\n'

        for converted_field in converted_fields:
            func_builder += self.__generate_set_property_field(converted_field)

        func_builder += '\t\treturn false;\n'

        func_builder += '\t}\n' 

        return func_builder

    def __generate_set_property_field(self, converted_field:ConvertedSchemaField):
        prefix = '\t\t'

        builder = ''
        builder += prefix + 'if (propertyName.Equals("{0}", StringComparison.OrdinalIgnoreCase))\n'.format(converted_field.field_name)
        builder += prefix + '{\n'
        builder += prefix + '\tif (CheckPropertyType({0}, ({1})value) == false)\n'.format(converted_field.field_name, converted_field.type_str)
        builder += prefix + '\t\t return false;\n'
        builder += prefix + '\t\t\n'
        builder += prefix + '\t{0} = ({1})value;\n'.format(converted_field.field_name, converted_field.type_str)
        builder += prefix + '\treturn true;\n' 
        builder += prefix + '}\n'

        return builder


class DartSchemaClassConverter(SchemaClassConverter):

    def __init__(self, excel_schema_data:ExcelSchemaData, db_extension:str):
        super().__init__(excel_schema_data, db_extension)
        self._convert_target_type = ConvertTargetType.Dart

    def generate(self):
        return self.__generate_class_unit()

    def generate_meta(self, meta_mapping_variable:str = 'GenerateTableMeta'):
        
        meta_builder = ''
        meta_builder += '{0}.addMeta<{1}>(\n'.format(meta_mapping_variable, self._excel_schema_data.table_name)
        meta_builder += '{0}'.format('TableMeta()')
        meta_builder += '..dbName = \'{0}{1}\''.format(self._excel_schema_data.db_name,self._db_extension)
        meta_builder += '..tableName = \'{0}\''.format(self._excel_schema_data.table_name)
        meta_builder += ');\n'

        return meta_builder

    def __generate_class_unit(self):
        
        table_name = self._excel_schema_data.table_name
        
        class_builder = ''
        class_builder += 'class {0} extends TblBase\n'.format(table_name)
        class_builder += '{\n'

        # Property Generate
        converted_fields = list(self.get_converted_fields())
        for converted_field in converted_fields:
            
            if converted_field.is_pk_field() == True:
                class_builder += self.__generate_pk_key_field(converted_field)
            else:
                class_builder += self.__generate_none_pk_key_field(converted_field)

        # Property Meta
        class_builder += '\n'
        class_builder += '\t@override\n'
        class_builder += '\tint get propertiesCount => {0};'.format(len(converted_fields))

        class_builder += '\n'
        class_builder += self.__generate_get_property_func(converted_fields)

        class_builder += '\n'
        class_builder += self.__generate_set_property_func(converted_fields)

        class_builder += '}\n'

        return class_builder

    def __generate_pk_key_field(self, converted_field:ConvertedSchemaField):
        
        default_context = converted_field.default_context
        default_context = default_context.replace('"', '\'')
        if len(default_context):
            default_context = '= {0}'.format(default_context)

        private_field_name = '_{0}'.format(converted_field.field_name)
        is_primary_key_str = 'true' if converted_field.is_primary else 'false'

        field_builder = ''
        field_builder += '\t{0} {1}{2};\n'.format(converted_field.type_str, private_field_name, default_context)
        field_builder += '\t{0} get {1} => {2};\n'.format(converted_field.type_str, converted_field.field_name, private_field_name)
        field_builder += '\tset {0}({1} value) {{\n'.format(converted_field.field_name, converted_field.type_str)
        field_builder += '\t\t{0} = value;\n'.format(private_field_name)
        field_builder += '\t\tconvertKey({0}, {1});\n'.format(private_field_name, is_primary_key_str)
        field_builder += '\t}\n'

        return field_builder

    def __generate_none_pk_key_field(self, converted_field:ConvertedSchemaField):

        default_context = converted_field.default_context
        default_context = default_context.replace('"', '\'')
        if len(default_context):
            default_context = ' = {0}'.format(default_context)

        return '\t{0} {1}{2};\n'.format(converted_field.type_str, converted_field.field_name, default_context)

    def __generate_get_property_func(self, converted_fields:list):
        func_builder = ''
        func_builder += '\t@override\n'
        func_builder += '\tTuple2<String, Type> getPropertyInfo(int index) {\n';

        func_builder += '\t\tswitch (index) {\n'

        for idx, converted_field in enumerate(converted_fields):
            func_builder += '\t\t\tcase {0}: return Tuple2(\'{1}\', {1}.runtimeType);\n'.format(idx, converted_field.field_name)

        func_builder += '\t\t}\n'

        func_builder += '\t\treturn null;\n' 
        func_builder += '\t}\n'

        return func_builder

    def __generate_set_property_func(self, converted_fields:list):
        func_builder = ''
        func_builder += '\t@override\n'
        func_builder += '\tbool setPropertyValueFromName<T>(String propertyName, T value) {\n'

        for converted_field in converted_fields:
            func_builder += self.__generate_set_property_field(converted_field)

        func_builder += '\t\treturn false;\n'

        func_builder += '\t}\n' 

        return func_builder

    def __generate_set_property_field(self, converted_field:ConvertedSchemaField):
        prefix = '\t\t'

        builder = ''
        builder += prefix + 'if (propertyName.toLowerCase() == \'{0}\') {{\n'.format(converted_field.field_name.lower())
        builder += prefix + '\tif (checkPropertyType({0}, value) == false) {{\n'.format(converted_field.field_name)
        builder += prefix + '\t\t return false;\n'
        builder += prefix + '\t}\n'
        builder += prefix + '\n'
        builder += prefix + '\t{0} = value as {1};\n'.format(converted_field.field_name, converted_field.type_str)
        builder += prefix + '\treturn true;\n' 
        builder += prefix + '}\n'

        return builder
