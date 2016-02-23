from distutils.core import setup
import os

dirname, filename = os.path.split(os.path.abspath(__file__))

setup(
        name='jdatetime',
        version='1.7.3',
        packages=['jdatetime',],
        license='Python Software Foundation License',
        keywords='Jalali implementation of Python datetime',
        platforms='any',
        description=("Jalali datetime binding for python"),
        url="https://github.com/slashmili/python-jalali",
        long_description=open(os.path.join(dirname, 'README.rst')).read()
)
