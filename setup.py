import setuptools
from distutils.core import setup


setup(
    name='jdatetime',
    version='3.7.0',
    packages=['jdatetime', ],
    license='Python Software Foundation License',
    keywords='Jalali implementation of Python datetime',
    platforms='any',
    author='Milad Rastian',
    author_email='eslashmili@gmail.com',
    description=("Jalali datetime binding for python"),
    url="https://github.com/slashmili/python-jalali",
    long_description=open('README').read(),
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development",
    ],
)
