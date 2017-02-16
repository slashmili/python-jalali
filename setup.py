from distutils.core import setup

setup(
        name='jdatetime',
        version='1.8.2',
        packages=['jdatetime',],
        license='Python Software Foundation License',
        keywords='Jalali implementation of Python datetime',
        platforms='any',
        author = 'Milad Rastian',
        author_email = 'eslashmili _at_ gmail.com',
        description=("Jalali datetime binding for python"),
        url="https://github.com/slashmili/python-jalali",
        long_description=open('README').read()
)
