# 
# This code is part of Aisle.
# 
# Aisle Version: 0.1.0
# 
# This file: aisle/_main.py
# Author(s): Yunheng Ma
# Timestamp: 2024-12-20 12:00:00 UTC
# 


"""
Module for interacting with AI.

This module provides functionality for an AI interaction interface, allowing 
users to send messages and manage conversation settings through Jupyter 
notebook cell and line magics.

Functions:
- ai: A cell magic function to interact with the AI.
- panel: A line magic function to manage the AI settings and display panels.
"""

import shlex
import argparse
import ipywidgets as widgets

from IPython.core.magic import register_line_magic
from IPython.core.magic import register_cell_magic

from ._logs import Logs
from ._backend import Backend
from ._messages import Messages
from ._source import update_backend, panel_status, panel_logs, panel_settings


__all__ = ["ai", "panel"]


# Initialize global instances for logging, backend, and message handling
backend = Backend()
logs = Logs()
messages = Messages()


@register_cell_magic
def ai(line: str, cell: str) -> None:
    """
    Interact with the AI using a Jupyter notebook cell magic.

    Parameters
    ----------
    line : str
        Command line arguments for configuring the AI interaction.
    cell : str
        The content of the cell to be processed by the AI.

    Returns
    -------
    None

    Examples
    --------
    %%ai --image path/to/image.png --format markdown --clear
    This is a prompt for the AI.
    """
    
    global backend, logs, messages

    # Parse command line arguments
    parser = argparse.ArgumentParser(prog='ai', description="Parse command arguments for AI.", exit_on_error=False)
    parser.add_argument('--image', type=str, help="Path to the input image.")
    parser.add_argument('--format', type=str, choices=['markdown', 'raw'], default='markdown',
                        help="Specify the output text rendering format.")
    parser.add_argument('--clear', '--clear-history', action='store_true', help="Forget previous conversation history.")
    
    args = parser.parse_args(shlex.split(line))
    
    # Clear message history if requested
    if args.clear:
        messages.clear()
        logs.info("Cleared session memory.")

    # Assemble messages for processing
    success, message = messages.assemble(cell, args.image)
    
    if success:
        logs.info(message)
    else:
        logs.error(message)
        return None
    
    # Send request to backend model and process result
    logs.info(f"Sending session request to {backend.model}.")
    success, message = messages.launch(backend)
    
    if success:
        logs.info(message)
    else:
        logs.error(message)
        return None

    # Display formatted output based on user preference
    if args.format == 'raw':
        messages.show(backend, raw=True)
    else:
        messages.show(backend)

    logs.info("AI response display completed.")

    
@register_line_magic
def panel(line: str) -> None:
    """
    Manage AI settings and display relevant panels using a Jupyter notebook line magic.

    Parameters
    ----------
    line : str
        Command line arguments for configuring the panel settings.

    Returns
    -------
    None

    Examples
    --------
    %panel --model new_model --seed 42 --temperature 0.7 --reproducible True
    """
    
    global logs, backend

    # Parse command line arguments for panel configuration
    parser = argparse.ArgumentParser(prog='panel', description="Parse command arguments for panel management.", exit_on_error=False)
    
    parser.add_argument('--model', '--set-model', type=str, help="Set the dialogue model.")
    parser.add_argument('--seed', '--set-seed', type=int, help="Set seed for reproducibility.")
    parser.add_argument('--temperature', '--set-temperature', type=float,
                        help="Set temperature for dialogue model in range [0.0, 1.0].")
    
    parser.add_argument('--reproducible', '--set-reproducible', type=bool,
                        help="Set dialogue reproducibility switch.")
    
    args = parser.parse_args(shlex.split(line))

    # Update backend settings if any parameter is provided
    if any(par is not None for par in [args.model, args.seed, args.temperature, args.reproducible]):
        update_backend(args, backend, logs)
    
    # Create and display panel tabs for status, settings, and logs
    status_tab = panel_status(backend)
    settings_tab = panel_settings(backend, logs)
    logs_tab = panel_logs(logs)

    tabs = widgets.Tab()
    
    # Assign children tabs to the widget and set titles
    tabs.children = [status_tab, settings_tab, logs_tab]
    tabs.set_title(0, "environment")
    tabs.set_title(1, "control")
    tabs.set_title(2, "logs")
    
    display(tabs)