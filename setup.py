from distutils.core import setup

setup(
        name='jdatetime',
        version='1.5',
        packages=['jdatetime',],
        license='Python Software Foundation License',
        keywords='Jalali implementation of Python datetime',
        platforms='any',
        long_description=open('README.txt').read(),
        description=("Jalali Date support for Django 1.7 "
                     "model and admin interface"),
        url="https://github.com/slashmili/python-jalali",
)
