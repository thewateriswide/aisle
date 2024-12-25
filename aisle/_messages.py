# 
# This code is part of Aisle.
# 
# Aisle Version: 0.1.0
# 
# This file: aisle/_messages.py
# Author(s): Yunheng Ma
# Timestamp: 2024-12-20 12:00:00 UTC
# 


"""
This module provides functionality for managing messages in a chat application.

It includes methods for assembling messages, launching requests to a backend,
and displaying messages with optional styling.
    
Classes:
- Messages: A class to manage chat messages and interactions with a 
  backend service.
"""

import requests
from typing import List, Dict, Any, Tuple
from IPython.display import display, Markdown

from ._general import generate_timestamp, temperature2color, image2base64
from ._backend import Backend


__all__ = ["Messages"]


class Messages:
    """
    A class to manage chat messages and interactions with a backend service.

    Attributes
    ----------
    messages : List[Dict[str, Any]]
        A list of messages exchanged in the chat.
    session_counter : int
        A counter to track the number of sessions.
    user_counter : int
        A counter to track the number of user messages.
    ai_counter : int
        A counter to track the number of AI responses.

    Methods
    -------
    assemble(content: str, image_path: str = None) -> Tuple[bool, str]:
        Assembles a user message and adds it to the message list.

    clear() -> None:
        Clears the message history and resets counters.

    launch(backend: Backend) -> Tuple[bool, str]:
        Sends the current messages to the backend and retrieves an AI response.

    show(backend: Backend, raw: bool = False) -> None:
        Displays the latest message with optional styling.
    """

    messages: List[Dict[str, Any]] = []
    session_counter = 1
    user_counter = 0
    ai_counter = 0

    def __add(self, message: Dict[str, Any]) -> None:
        """Adds a message to the message list.

        Parameters
        ----------
        message : Dict[str, Any]
            The message to be added.
        """
        
        self.messages.append(message)

    def assemble(self, content: str, image_path: str = None) -> Tuple[bool, str]:
        """Assembles a user message and adds it to the message list.

        Parameters
        ----------
        content : str
            The content of the user message.
        image_path : str, optional
            The path to an image file (default is None).

        Returns
        -------
        Tuple[bool, str]
            A tuple indicating success and a message.
        
        Examples
        --------
        >>> msg = Messages()
        >>> msg.assemble("Hello!", "path/to/image.png")
        (True, "User content has been loaded.")
        """
        
        user_message = {'role': 'user', 'content': content}
        
        if image_path:
            success, result = image2base64(image_path)
            if success:
                code = result
                user_message.update({'images': [code]})
            else:
                error_message = result
                return (False, error_message)

        self.__add(user_message)
        self.user_counter += 1
        return (True, "User content has been loaded.")

    def clear(self) -> None:
        """Clears the message history and resets counters."""
        
        self.messages.clear()
        self.session_counter += 1
        self.user_counter = 0
        self.ai_counter = 0

    def launch(self, backend: Backend) -> Tuple[bool, str]:
        """Sends the current messages to the backend and retrieves an AI response.

        Parameters
        ----------
        backend : Backend
            The backend instance used for sending requests.

        Returns
        -------
        Tuple[bool, str]
            A tuple indicating success and a message.
        
        Examples
        --------
        >>> backend_instance = Backend(...)
        >>> msg.launch(backend_instance)
        (True, "AI response has been received.")
        
        Raises
        ------
        requests.RequestException
            If there is an error during the request.
        """
        
        data = {
            'model': backend.model,
            'messages': self.messages,
            'stream': backend.stream,
            'options': {'temperature': backend.temperature},
        }
        
        if backend.reproducible:
            data['options']['seed'] = backend.seed
            
        try:
            response = requests.post(url=f"{backend.url}api/chat", json=data)
            response.raise_for_status()
            response_data = response.json()
            
            if 'message' in response_data:
                ai_message = response_data['message']
                self.__add(ai_message)
                self.ai_counter += 1
                return (True, "AI response has been received.")
            else:
                return (False, "The 'message' field was not found in the response.")
                
        except requests.RequestException as e:
            return (False, f"An error occurred while requesting the backend: {e}")
          
    def show(self, backend: Backend, raw: bool = False) -> None:
        """Displays the latest message with optional styling.
        
        Parameters
        ----------
        backend : Backend
            The backend instance used for retrieving temperature color.
        
        raw : bool, optional
            If True, displays raw content; otherwise displays styled output (default is False).
        
        Examples
        --------
        >>> msg.show(backend_instance)
        
        Notes
        -----
        This method will only display content if there are messages present.
        If no messages are available, it will not output anything.
        """
        
        # Only display if there are messages present.
        if self.messages:  
            temperature_color = temperature2color(backend.temperature)
            content = self.messages[-1]['content']
        else:
            return None

        if raw:
            print(content)
        else:
            color_blocks = (
            "<div style='display: flex; justify-content: left; gap: 0px; margin-bottom: -6px; margin-left: 28px'>"
            "<div style='width: 8px; height: 8px; background-color: #118ab2; border-radius: 4px; margin: 1.5px; z-index: 2;'></div>"
            "<div style='width: 8px; height: 8px; background-color: #ef476f; border-radius: 4px; margin: 1.5px; z-index: 2;'></div>"
            "<div style='width: 8px; height: 8px; background-color: #7f5539; border-radius: 4px; margin: 1.5px; z-index: 2;'></div>"
            "</div>"
            )
        
            styled_div = (
            # f"{color_blocks}"
            f"<div style='display: flex; align-items: stretch; width: 100%'>"
            f"<div style='border-left: 8px solid {temperature_color}; border-radius: 2px; margin-right: 4px;'></div>"
            f"<div style='flex: 1; border: 1.5px solid darkgray; border-radius: 0px; padding: 8px; z-index: 1;'>"
            f"{content}"
            f"</div>"
            f"</div>"
            )
        
            print(f" \033[97m Date:[{generate_timestamp()}]  Session:[{self.session_counter}.{self.ai_counter}]\033[0m")
            display(Markdown(styled_div))