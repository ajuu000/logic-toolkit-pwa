"""
Logic Pro Toolkit - Python automation and utilities

A comprehensive toolkit for working with Logic Pro files and automation.
"""
from .client import LogicProClient
from .processor import LogicProProcessor
from .metadata import LogicProMetadataReader
from .batch import BatchProcessor
from .exporter import DataExporter

__version__ = "0.1.0"
__author__ = "Open Source Community"

__all__ = [
    "LogicProClient",
    "LogicProProcessor",
    "LogicProMetadataReader",
    "BatchProcessor",
    "DataExporter",
]
