# setup.py

from setuptools import setup, find_packages

setup(
    name="DIYables_MicroPython_OLED",
    version="0.1.2",
    description="MicroPython Library for OLED display, created by DIYables",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="DIYables",
    author_email="DIYables.io@gmail.com",
    url="https://diyables.io",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: Implementation :: MicroPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
