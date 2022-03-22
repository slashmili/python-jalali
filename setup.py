from distutils.core import setup

import setuptools

setup(
    name='jdatetime',
    version='4.1.0',
    packages=['jdatetime', ],
    license='Python Software Foundation License',
    keywords='Jalali implementation of Python datetime',
    platforms='any',
    author='Milad Rastian',
    author_email='eslashmili@gmail.com',
    description=("Jalali datetime binding for python"),
    url="https://github.com/slashmili/python-jalali",
    long_description=open('README').read(),
    python_requires=">=3.7",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development",
    ],
)
