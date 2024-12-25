# 
# This code is part of Aisle.
# 
# Aisle Version: 0.1.0
# 
# This file: aisle/_general.py
# Author(s): Yunheng Ma
# Timestamp: 2024-12-20 12:00:00 UTC
# 


"""
Module for image processing and model retrieval.

This module provides functions to generate timestamps, retrieve model lists 
from a specified URL, convert temperature values to color representations, and
encode images in base64 format.

Functions:
- generate_timestamp: Generates a timestamp in UTC format.
- get_model_list: Fetches a list of models from a given API URL.
- temperature2color: Converts a temperature value to its corresponding color 
  in hexadecimal format.
- image2base64: Encodes images in base64 format.
"""

import os
import base64
import requests

from matplotlib import pyplot as plt
from datetime import datetime, timezone
from typing import List, Tuple


__all__ = ["generate_timestamp",
           "get_model_list",
           "temperature2color",
           "image2base64",
           ]


def generate_timestamp() -> str:
    """
    Generate a timestamp in UTC format.

    Returns
    -------
    str
        The current timestamp formatted as 'YYYY-MM-DD HH:MM:SS.sss UTC'.

    Examples
    --------
    >>> generate_timestamp()
    '2020-02-20 14:00:00.000 UTC'
    """
    
    current_time = datetime.now(timezone.utc)
    return current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + " UTC"


def get_model_list(url: str) -> Tuple[bool, List[str] | str]:
    """
    Retrieve a list of model names from the specified API URL.

    Parameters
    ----------
    url : str
        The base URL of the API.

    Returns
    -------
    Tuple[bool, Union[List[str], str]]
        A tuple where the first element indicates success or failure,
        and the second element is either a list of model names or an error message.

    Examples
    --------
    >>> get_model_list('http://example.com/')
    (True, ['model1', 'model2'])
    """
    
    try:
        response = requests.get(url + 'api/tags', timeout=5)
        response.raise_for_status()  # Check if the request was successful
        models = response.json().get('models', [])
        return (True, [item['name'] for item in models])
    
    except requests.RequestException as e:
        return (False, f"Error occurred while accessing model list: {e}")
    
    except ValueError as e:
        return (False, f"Error occurred while parsing model list: {e}")


def temperature2color(temperature: float) -> str:
    """
    Convert a temperature value to its corresponding color in hexadecimal format.

    Parameters
    ----------
    temperature : float
        A temperature value expected to be in the range [0, 1].

    Returns
    -------
    str
        The hexadecimal color representation of the temperature.

    Examples
    --------
    >>> temperature2color(0.5)
    '#cb4777'
    """
    
    # Normalize temperature value between 0 and 1
    normalized_value = max(0, min(temperature, 1))
    
    # Get the 'plasma' colormap; can be changed to 'viridis' or other available colormaps
    cmap = plt.get_cmap('plasma')  
    rgba = cmap(normalized_value)
    
    # Convert RGBA to hexadecimal color string
    hex_color = f'#{int(rgba[0] * 255):02x}{int(rgba[1] * 255):02x}{int(rgba[2] * 255):02x}'
    
    return hex_color


def image2base64(image_path: str) -> Tuple[bool, str]:
    """
    Encode an image file at the specified path into base64 format.
    
    Parameters
    ----------
    image_path : str
        The file path of the image to encode.
    
    Returns
    -------
    Tuple[bool, str]
        A tuple where the first element indicates success or failure,
        and the second element is either the base64 encoded string or an error message.
    
    Examples
    --------
    >>> image2base64('path/to/image.jpg')
    (True, 'base64_encoded_string_here')
    
    >>> image2base64('invalid/path.jpg')
    (False, "Image file 'invalid/path.jpg' not found.")
    
    """
    
    valid_extensions = ('.jpg', '.jpeg', '.png')  # Supported image formats
    
    # Validate input path
    if not isinstance(image_path, str) or not image_path.strip():
       return (False, "The specified image path is invalid.")
    
    # Validate file extension
    if not image_path.lower().endswith(valid_extensions):
       return (False, f"The file '{image_path}' is not a valid image format. Supported formats are: {', '.join(valid_extensions)}.")
    
    # Validate if file exists
    if not os.path.isfile(image_path):
       return (False, f"Image file '{image_path}' not found.")
        
    try:
       # Open and read the image file
       with open(image_path, 'rb') as img:
           encoded_img = base64.b64encode(img.read()).decode('utf-8')  # Encode image to base64
            
           return (True, encoded_img)
    
    except IOError as e:
       return (False, f"Error occurred while opening the file: {e}")