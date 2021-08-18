import numpy
from parser.enum_define_parser import EnumMetaInfo

# schema type에 맞는 범위인가 체크하는 함수들

#int32 체크
def is_valid_value_int32(value, *arg):

        type_value = value
        if isinstance(value, str) == True and value.isnumeric() == True:
            type_value = numpy.int32(value)

        if isinstance(type_value, int) == False:
            return False

        int32iinfo = numpy.iinfo(numpy.int32)

        if type_value < int32iinfo.min or type_value > int32iinfo.max:
            return False

        return True

#uint32 체크
def is_valid_value_uint32(value, *arg):

    type_value = value
    if isinstance(value, str) == True and value.isnumeric() == True:
        try:
            type_value = numpy.uint32(value)
        except:
            return False

    if isinstance(type_value, int) == False:
       return False

    uint32iinfo = numpy.iinfo(numpy.uint32)

    if type_value < uint32iinfo.min or type_value > uint32iinfo.max:
        return False

    return True

#float32 체크
def is_valid_value_float32(value, *arg):

    type_value = value
    if isinstance(value, str) == True and value.isnumeric() == True:
        try:
            type_value = numpy.uint32(value)
        except:
            return False

    if isinstance(type_value, float) == False:
        return False

    uint32iinfo = numpy.iinfo(numpy.uint32)

    if type_value < uint32iinfo.min or type_value > uint32iinfo.max:
        return False

    return True

#bool 체크
def is_valid_value_bool(value, *arg):
    type_value = value
    if isinstance(value, str) == True:
        try:
            type_value = bool(value)
        except:
            return False

    if isinstance(type_value, bool) == False:
        return False

    return True

#Enum 체크
def is_valid_value_enum(value, enum_meta_info:EnumMetaInfo):

    if enum_meta_info is None:
        return False

    if isinstance(value, str) == False:
        return False

    return enum_meta_info.is_exist_enum_field(value)
