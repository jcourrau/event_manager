from setuptools import setup, find_packages

setup(
    name="event_manager",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "python-dateutil",
        "pytz",
        "tzdata",
        "SqlAlchemy",
    ],
    description="A module for managing recurring events.",
    author="Jason Courrau",
    author_email="jasoncourrau@gmail.com",
    license="MIT"
)
