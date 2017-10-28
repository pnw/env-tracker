from setuptools import setup


setup(
    name='et',
    version='0.1',
    py_modules=['main'],
    install_requires=[
        'Click',
    ],
    entry_points = '''
    [console_scripts]
    et=main:et
    '''
)
