from setuptools import setup, find_packages

from typerighter import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='typerighter',
    version=__version__,
    author='Jms Dnns',
    author_email='jdennis@gmail.com',
    description='Data Types for Cynical Humans',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/jmsdnns/typerighter',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'pycodestyle',
            'pylint',
            'tox'
        ], 
        'docs': [
            'sphinx',
            'doc8'
        ]
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only', 
    ]
)
