from enum import Enum

class ConvertTargetType(Enum):
    Empty = 0
    CSharp = 1
    Dart = 2

    @staticmethod
    def get_string(type):
        if type is ConvertTargetType.CSharp:
            return 'csharp'
        
        if type is ConvertTargetType.Dart:
            return 'dart'

        return ''
