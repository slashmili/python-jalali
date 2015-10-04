from distutils.core import setup

setup(
        name='jdatetime',
        version='1.7',
        packages=['jdatetime',],
        license='Python Software Foundation License',
        keywords='Jalali implementation of Python datetime',
        platforms='any',
        long_description=open('README.txt').read(),
        description=("Jalali datetime binding for python"),
        url="https://github.com/slashmili/python-jalali",
)
