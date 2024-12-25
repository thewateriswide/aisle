# 
# This code is part of Aisle.
# 
# Aisle Version: 0.1.0
# 
# This file: aisle/_source.py
# Author(s): Yunheng Ma
# Timestamp: 2024-12-20 12:00:00 UTC
# 


"""
Module for managing backend updates and UI panels for settings and controls.

This module provides functions to update backend parameters, display status 
and logs, and manage user input through interactive widgets.

Functions:
- update_backend: Updates the backend with model, seed, temperature, and 
  reproducibility settings.
- panel_status: Creates a panel to display the current status of the backend.
- panel_logs: Creates a panel to display logs.
- panel_model_setting: Creates a dropdown for selecting models.
- panel_seed_setting: Creates an input field for setting the random seed.
- panel_reproducible_setting: Creates a checkbox for reproducibility settings.
- panel_temperature_setting: Creates an input field for setting the temperature.
- panel_settings: Combines all settings panels into one.
"""

import argparse
import ipywidgets as widgets

from ._general import temperature2color, get_model_list
from ._logs import Logs
from ._backend import Backend


__all__ = ["update_backend", 
           "panel_status", 
           "panel_settings",
           "panel_logs", 
           ]


def update_backend(args: argparse.Namespace, backend: Backend, logs: Logs) -> None:
    """
    Update the backend parameters based on user input from command line arguments.

    Parameters
    ----------
    args : argparse.Namespace
        Command line arguments containing model, seed, temperature, and reproducibility settings.
    backend : Backend
        The backend instance responsible for managing the model and its parameters.
    logs : Logs
        The logs instance for logging messages related to updates.

    Returns
    -------
    None

    Examples
    --------
    >>> update_backend(args, backend_instance, logs_instance)
    """
    
    # Update model parameter
    if args.model:
        success, message = backend.update_model(args.model)
        logs.info(message) if success else logs.error(message)

    # Update random seed
    if args.seed is not None:
        success, message = backend.update_seed(args.seed)
        logs.info(message) if success else logs.error(message)

    # Update temperature parameter
    if args.temperature is not None:
        success, message = backend.update_temperature(args.temperature)
        logs.info(message) if success else logs.error(message)
            
    # Update reproducibility parameter
    if args.reproducible is not None:
        success, message = backend.update_reproducible(args.reproducible)
        logs.info(message) if success else logs.error(message)


def panel_status(backend: Backend) -> widgets.VBox:
    """
    Create a panel to display the current status of the backend.

    Parameters
    ----------
    backend : Backend
        The backend instance responsible for managing the model and its parameters.

    Returns
    -------
    widgets.VBox
        A VBox widget containing a refresh button and the output area displaying the status.

    Examples
    --------
    >>> status_panel = panel_status(backend_instance)
    """
    
    output = widgets.Output()
    
    with output:
        backend.show()
    
    def refresh(click):
        """Refresh the output area with current status."""
        output.clear_output()
        with output:
            backend.show()
    
    button = widgets.Button(description='Refresh')
    button.style.button_color = 'lightblue'
    button.on_click(refresh)
    
    return widgets.VBox([button, output])


def panel_logs(logs: Logs) -> widgets.VBox:
    """
    Create a panel to display logs.

    Parameters
    ----------
    logs : Logs
        The logs instance for logging messages.

    Returns
    -------
    widgets.VBox
        A VBox widget containing a refresh button and the output area displaying logs.

    Examples
    --------
    >>> logs_panel = panel_logs(logs_instance)
    """
    
    output = widgets.Output()
    
    with output:
        logs.show()
    
    def refresh(click):
        """Refresh the output area with current logs."""
        output.clear_output()
        with output:
            logs.show()
    
    button = widgets.Button(description='Refresh')
    button.style.button_color = 'lightblue'
    button.on_click(refresh)
    
    return widgets.VBox([button, output])


def panel_model_setting(backend: Backend, logs: Logs) -> widgets.Dropdown:
    """
    Create a dropdown menu for selecting models.
    
    Parameters
    ----------
    backend : Backend
        The backend instance responsible for managing models.
        
    logs : Logs
        The logs instance for logging messages.
    
    Returns
    -------
    widgets.Dropdown
       A dropdown widget for selecting models.
    
    Examples
    ---------
    >>> model_dropdown = panel_model_setting(backend_instance, logs_instance)
    """
    
    success, result = get_model_list(backend.url)
    
    model_list = result if success else []
    
    if not success:
       error_message = result
       logs.error(error_message)
    
    dropdown = widgets.Dropdown(
       options=model_list,
       value=backend.model,
       description='model:'
    )
    
    def set_model(new_model: str):
        """Set the selected model in the backend."""
        success, message = backend.update_model(new_model)
        logs.info(message) if success else logs.error(message)
    
    dropdown.observe(lambda change: set_model(change['new']), names='value')
    
    return dropdown


def panel_seed_setting(backend: Backend, logs: Logs) -> widgets.IntText:
    """
    Create an input field for setting the random seed.
    
    Parameters
    ----------
    backend : Backend
       The backend instance responsible for managing parameters.
       
    logs : Logs
       The logs instance for logging messages.
    
    Returns
    -------
    widgets.IntText
       An IntText widget for entering the random seed.
    
    Examples
    ---------
    >>> seed_input = panel_seed_setting(backend_instance, logs_instance)
    """
    
    int_text = widgets.IntText(value=backend.seed, description='seed:')
    
    def set_seed(new_seed: int):
        """Set the random seed in the backend."""
        success, message = backend.update_seed(new_seed)
        logs.info(message) if success else logs.error(message)
    
    int_text.observe(lambda change: set_seed(change['new']), names='value')
    
    return int_text

    
def panel_reproducible_setting(backend: Backend, logs: Logs) -> widgets.Checkbox:
    """
    Create a checkbox for enabling reproducibility settings.
    
    Parameters
    ----------
    backend : Backend
       The backend instance responsible for managing parameters.
       
    logs : Logs
       The logs instance for logging messages.
    
    Returns
    -------
    widgets.Checkbox
       A Checkbox widget for reproducibility settings.
    
    Examples
    ---------
    >>> reproducible_checkbox = panel_reproducible_setting(backend_instance, logs_instance)
    """
    
    checkbox = widgets.Checkbox(description='reproducible', value=backend.reproducible)
    
    def set_reproducible(new_reproducible: bool):
        """Set reproducibility in the backend."""
        success, message = backend.update_reproducible(new_reproducible)
        logs.info(message) if success else logs.error(message)
    
    checkbox.observe(lambda change: set_reproducible(change['new']), names='value')
    
    return checkbox


def panel_temperature_setting(backend: Backend, logs: Logs) -> widgets.HBox:
    """
    Create an input field and color square for setting temperature.
    
    Parameters
    ----------
    backend : Backend 
       The backend instance responsible for managing parameters.
       
    logs : Logs 
       The logs instance for logging messages.
    
    Returns 
    -------
    widgets.HBox 
       An HBox widget containing an input field and color square for temperature.
    
    Examples 
    ---------
    >>> temperature_hbox = panel_temperature_setting(backend_instance, logs_instance)
    """
    
    def set_temperature(new_temperature: float):
        """Set temperature in the backend."""
        success, message = backend.update_temperature(new_temperature)
        logs.info(message) if success else logs.error(message)
    
    def refresh_square(new_temperature: float):
        """Refresh color square based on current temperature."""
        output.clear_output()
        color = temperature2color(new_temperature)
        square_html = f"<div style='width: 22px; height: 22px; border: 0.5px solid black; background-color: {color};'></div>"
        with output:
           display(widgets.HTML(value=square_html))
    
    float_text = widgets.FloatText(value=backend.temperature, description='temperature:', step=0.1)
    
    output = widgets.Output()
    
    refresh_square(backend.temperature)
    
    def on_temperature_change(change):
        """Handle changes in temperature input."""
        set_temperature(change['new'])
        refresh_square(change['new'])

    float_text.observe(on_temperature_change, names='value')
    
    return widgets.HBox([float_text, output])


def panel_settings(backend: Backend, logs: Logs) -> widgets.VBox:
    """
    Combine all settings panels into one VBox widget.
    
    Parameters
    ----------
    backend : Backend 
      The backend instance responsible for managing parameters.
      
    logs : Logs 
      The log instance used to log messages during updates.
    
    Returns 
    -------
    widgets.VBox 
      A VBox widget containing all individual setting panels.
    
    Examples 
    ---------
    >>> settings_panel = panel_settings(backend_instance, logs_instance)
    """
    
    model_dropdown = panel_model_setting(backend, logs)
    seed_int_text = panel_seed_setting(backend, logs)
    reproducible_checkbox = panel_reproducible_setting(backend, logs)
    temperature_hbox = panel_temperature_setting(backend, logs)
    
    return widgets.VBox([model_dropdown, seed_int_text, reproducible_checkbox, temperature_hbox])