# 
# This code is part of Aisle.
# 
# Aisle Version: 0.1.0
# 
# This file: aisle/_logs.py
# Author(s): Yunheng Ma
# Timestamp: 2024-12-20 12:00:00 UTC
# 


"""
Logging module for capturing and displaying log messages with severity levels.

This module provides a Logs class that allows for logging messages at various 
levels (info, warning, error), storing them in memory, and displaying them in 
a formatted manner.

Classes:
- Logs: A class to log messages with different severity levels.
"""

from typing import List

from ._general import generate_timestamp


__all__ = ["Logs"]


class Logs:
    """
    A class to log messages with different severity levels.
    
    This class provides methods to log informational, warning, and error messages.
    Each log entry is stored in memory with a timestamp and can be displayed
    in a formatted manner. This is useful for tracking application behavior
    and debugging.
    
    Attributes
    ----------
    logs : List[dict]
        A list to store log entries, where each entry is a dictionary containing
        the log level, timestamp, and message.
    
    Methods
    -------
    info(message: str) -> None:
        Log an informational message.
        
    warning(message: str) -> None:
        Log a warning message and print it to the console.
        
    error(message: str) -> None:
        Log an error message and print it to the console.
        
    show(item_number: int = 20) -> None:
        Display the most recent log entries.
    """

    logs: List[dict] = []

    def info(self, message: str) -> None:
        """
        Log an informational message.

        Parameters
        ----------
        message : str
            The message to log as informational.

        Returns
        -------
        None
        """
        
        timestamp_str = generate_timestamp()
        self.logs.append({"level": 'I', "timestamp": timestamp_str, "message": message})

    def warning(self, message: str) -> None:
        """
        Log a warning message and print it to the console.

        Parameters
        ----------
        message : str
            The message to log as a warning.

        Returns
        -------
        None
        """
        
        timestamp_str = generate_timestamp()
        self.logs.append({"level": 'W', "timestamp": timestamp_str, "message": message})
        print(f'\033[33m[W {timestamp_str}]\033[0m {message}')

    def error(self, message: str) -> None:
        """
        Log an error message and print it to the console.

        Parameters
        ----------
        message : str
            The message to log as an error.

        Returns
        -------
        None
        """
        
        timestamp_str = generate_timestamp()
        self.logs.append({"level": 'E', "timestamp": timestamp_str, "message": message})
        print(f'\033[31m[E {timestamp_str}]\033[0m {message}')

    def show(self, item_number: int = 20) -> None:
        """
        Display the most recent log entries.

        Parameters
        ----------
        item_number : int, optional
            The number of recent log entries to display (default is 20).

        Returns
        -------
        None
        """
        
        items = []
        
        if not self.logs:
            items.append('\033[90m(No logs available)\033[0m')
        else:
            recent_logs = self.logs[-item_number:] if len(self.logs) > item_number else self.logs
            items.append(f"\033[90m(Displaying the most recent {item_number} records)\033[0m")

            for log in recent_logs:
                color = {'I': '32', 'W': '33', 'E': '31'}.get(log['level'], '30')  # Default to black color
                items.append(f"\033[{color}m[{log['level']} {log['timestamp']}]\033[0m {log['message']}")
                
        for item in items:
            print(item)  # Display logs.