from distutils.core import setup

REQUIRES = (
        'six==1.12.0',
)

setup(
        name='jdatetime',
        version='3.2.0',
        packages=['jdatetime',],
        license='Python Software Foundation License',
        keywords='Jalali implementation of Python datetime',
        platforms='any',
        author = 'Milad Rastian',
        install_requires=REQUIRES,
        author_email = 'eslashmili@gmail.com',
        description=("Jalali datetime binding for python"),
        url="https://github.com/slashmili/python-jalali",
        long_description=open('README').read()
)
