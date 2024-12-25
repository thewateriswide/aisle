# 
# This code is part of Aisle.
# 
# Aisle Version: 0.1.0
# 
# This file: aisle/_backend.py
# Author(s): Yunheng Ma
# Timestamp: 2024-12-20 12:00:00 UTC
# 


"""
Backend module for managing model configurations and settings.

This module provides the Backend class, which allows users to interactwith a 
specific model's settings, including updating the model, seed,temperature, and
reproducibility status. It also provides a method todisplay the current 
settings in a formatted manner.

Classes:
- Backend: A class to manage the backend model configuration.
"""

from typing import Tuple
from IPython.display import display, Markdown

from ._general import get_model_list


__all__ = ["Backend"]


class Backend:
    """
    A class to manage the backend model configuration.

    Attributes
    ----------
    url : str
        The API address for the backend.
    model : str
        The current model name being used.
    stream : bool
        The status of streaming output.
    seed : int
        The seed value for reproducibility.
    temperature : float
        The temperature setting for the model.
    reproducible : bool
        Indicates whether the conversation is reproducible.

    Methods
    -------
    update_model(new_model: str) -> Tuple[bool, str]:
        Updates the current model to a new one if valid.
    
    update_seed(new_seed: int) -> Tuple[bool, str]:
        Updates the conversation seed to a new integer value.
    
    update_reproducible(new_reproducible: bool) -> Tuple[bool, str]:
        Updates the reproducibility status.
    
    update_temperature(new_temperature: float) -> Tuple[bool, str]:
        Updates the temperature setting within a specified range.
    
    show() -> None:
        Displays the current settings in a formatted Markdown table.
    """

    __url: str = 'http://example.com/aisle/'
    __model: str = 'model:default'
    __stream: bool = False
    __seed: int = 0
    __temperature: float = 0.4
    __reproducible: bool = False

    @property
    def url(self) -> str:
        """Get the API address."""
        return self.__url

    @property
    def model(self) -> str:
        """Get the current model name."""
        return self.__model

    @property
    def stream(self) -> bool:
        """Get the streaming output status."""
        return self.__stream

    @property
    def seed(self) -> int:
        """Get the current conversation seed."""
        return self.__seed

    @property
    def temperature(self) -> float:
        """Get the current temperature value."""
        return self.__temperature

    @property
    def reproducible(self) -> bool:
        """Get the reproducibility status."""
        return self.__reproducible

    def update_model(self, new_model: str) -> Tuple[bool, str]:
        """
        Update the current model to a new one if valid.

        Parameters
        ----------
        new_model : str
            The name of the new model to set.

        Returns
        -------
        Tuple[bool, str]
            A tuple containing a success flag and a message.
        """
        
        success, vals = get_model_list(self.__url)
        
        if not success:
            return (False, vals)
        
        if new_model in vals:
            self.__model = new_model
            return (True, f"Changed backend model to {self.__model}.")
        
        else:
            return (False, f"Model {new_model} is invalid, update failed.")

    def update_seed(self, new_seed: int) -> Tuple[bool, str]:
        """
        Update the conversation seed to a new integer value.

        Parameters
        ----------
        new_seed : int
            The new seed value.

        Returns
        -------
        Tuple[bool, str]
            A tuple containing a success flag and a message.
        """
        
        if not isinstance(new_seed, int):
            return (False, f"Seed {new_seed} type error, must be an integer (int).")
            
        self.__seed = new_seed
        return (True, f"Seed is now set to {self.__seed}.")

    def update_reproducible(self, new_reproducible: bool) -> Tuple[bool, str]:
        """
        Update the reproducibility status.

        Parameters
        ----------
        new_reproducible : bool
            The new reproducibility status.

        Returns
        -------
        Tuple[bool, str]
            A tuple containing a success flag and a message.
        """
        
        if not isinstance(new_reproducible, bool):
            return (False, f"Reproducibility {new_reproducible} type error, must be boolean (bool).")
            
        self.__reproducible = new_reproducible
        return (True, f"Conversation reproducibility has been set to {'enabled' if self.__reproducible else 'disabled'}.")

    def update_temperature(self, new_temperature: float) -> Tuple[bool, str]:
        """
        Update the temperature setting within a specified range.
        
        Parameters
        ----------
        new_temperature : float
            The desired temperature value.
        
        Returns
        -------
        Tuple[bool, str]
            A tuple containing a success flag and a message.
        
        Notes:
        ------
        Temperature values are clamped between 0.0 and 1.0.
        """
        
        if not isinstance(new_temperature, float):
         return (False, f"Temperature {new_temperature} type error, must be a float.")
        
        # Limit temperature between 0 and 1 
        value = max(0., min(new_temperature, 1.))  
        self.__temperature = value        
        return (True, f"Temperature is now set to {self.__temperature}.")

    def show(self) -> None:
        """
        Display the current settings in a formatted Markdown table.
        
        Returns
        -------
        None 
        """
        
        chars = []
        
        chars.append(2 * '| ' + '|')
        chars.append(2 * '|-' + '|')
        
        chars.append(f"|**model**|{self.__model}|")
        chars.append(f"|**temperature**|{self.__temperature}|")
        chars.append(f"|**reproducible**|{self.__reproducible}|")
        chars.append(f"|**seed**|{self.__seed}|")
        
        sheet = '\n '.join(chars)
        
        display(Markdown(sheet))