from os import system, sys

code = lambda module : f"""
try:
    import {module}
except ModuleNotFoundError:
    print(f'[ERROR] : {module} not installed properly')
"""

modules = open('requirements.txt','r').read().split('\n')

for module in modules:
    if module:
        if sys.platform == 'win32':
            system(f'pip install {module}')
        module = module.split('=')[0]
        if sys.platform == 'linux':
            system(f'pip install {module}')
        module = module.split('-')[0]
        system(f'python -c "{code(module)}"')