"""
Oman Economic Analysis Package

A comprehensive analysis of Oman's economic indicators using World Bank data.
"""

from .data_collector import OmanDataCollector
from .data_processor import DataProcessor
from .visualizations import EconomicVisualizer

__version__ = "1.0.0"
__author__ = "Ahmed"

__all__ = [
    "OmanDataCollector",
    "DataProcessor",
    "EconomicVisualizer"
]
