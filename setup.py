# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:25:44 2024

@author: dcr
"""

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='punxa_atmega328p',  # Updated to your chosen PyPI package name
    version='2026.1.0',       # Updated version format (Semantic Versioning recommended for PyPI)
    author='David Castells-Rufas',
    author_email='david.castells@uab.cat',
    description='Python-based ATmega328P Hardware Simulation and Tools.', # Updated description
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/davidcastells/punxa_atmega328p', # Keep or update to specific repo branch if needed
    install_requires=[
        'py4hw>=2025.4', 
        'pyelftools', 
        'itanium-demangler'
    ],
    # Note: tests_require is deprecated in modern setuptools. 
    # Use extras_require if you need specific test dependencies.
    extras_require={
        'test': ['pytest'], 
    },
    packages=find_packages(),
    package_data={'': ['*.png', '*.bin', '*.hex']}, # Added potential microcontroller hex/bin files
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", # Adjust to match your actual license
        "Operating System :: OS Independent",
        "Topic :: System :: Hardware",
    ],
    python_requires='>=3.7',
)