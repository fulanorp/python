from cx_Freeze import setup, Executable

executables = [Executable('Checklist.py', base=None) ]

setup(
    name='CheckList',
    version='1.0',
    description='Check de atividades App Lojas',
    executables=executables
)
