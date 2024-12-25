# 
# This code is part of Aisle.
# 
# Aisle Version: 0.1.0
# 
# This file: aisle/__init__.py
# Author(s): Yunheng Ma
# Timestamp: 2024-12-20 12:00:00 UTC
# 


"""
This module serves as the package initializer for the AI interaction interface.

Aisle is a tool for interacting with AI in Jupyter Notebook. It provides an 
easy-to-use interface that allows users to send messages, manage conversation 
history, and set dialogue parameters.

Functions:
- ai: A cell magic function to interact with the AI.
- panel: A line magic function to manage AI settings and display panels.
"""

__version__ = "0.1.0"
__author__ = "Yunheng Ma"

# Public API of the module
__all__ = ["ai", "panel"]

from ._main import ai, panel