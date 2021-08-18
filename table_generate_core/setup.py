from setuptools import setup

setup(name = 'parser',
    description='excelschema, exceldata, enum parser',
    version='0.0.1',
    setup_requires=['py2app'],
    app=['main.py'],
    options={
        'py2app': {
            'includes' : [
                'PySide.QtCore',
                'PySide.QtGui',
                'PySide.QtWebKit',
                'PySide.QtNetwork',
                'PySide.QtXml'
            ]
        }
    })