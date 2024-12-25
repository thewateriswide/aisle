Welcome to the Aisle Python package! Aisle is a powerful tool designed to help users interact with AI within Jupyter Notebooks. This document will guide you through using Aisle's two main features: `ai` and `panel`.

## Installation and Configuration

Before getting started, ensure that you have properly installed the Aisle package.

## Using Aisle

The following command can be used to import Aisle:

```python
from aisle import *
```

Aisle provides two primary magic commands that allow you to interact with AI in a Jupyter Notebook.

### 1. `%%ai` Magic Command

The `%%ai` command is used to send messages to the AI and receive its response. You can configure some parameters as needed.

#### Usage Example

```python
%%ai --image path/to/image.png --clear
Hello, how's the weather today?
```

#### Parameter Description

- `--image <path>`: Specifies the path of the input image (optional).
- `--format <markdown|raw>`: Sets the rendering format for output text; default is `markdown`.
- `--clear`: Clears previous conversation records.

#### Functionality Overview

- **Send Message**: This command allows you to send a text message to the AI and receive its response.
- **Manage Conversation History**: Using the `--clear` parameter, you can clear previous conversation records and start a new session.

### 2. `%panel` Magic Command

The `%panel` command is used to set conversation parameters and display a control panel.

#### Usage Example

```python
%panel --model qwen2.5:14b --temperature 0.7
```

#### Parameter Description

- `--model <model_name>`: Sets the dialogue model, e.g., `qwen2.5:14b`.
- `--seed <int>`: Sets the random seed; only effective when reproducibility is enabled.
- `--temperature <float>`: Sets the temperature of the dialogue model, ranging from [0.0, 1.0].
- `--reproducible <bool>`: Toggles the reproducibility switch.

#### Functionality Overview

- **Set Dialogue Parameters**: This command allows you to flexibly adjust the behavior and response style of AI.
- **Display Panel**: After executing this command, a tab panel containing session environment settings and runtime logs will be displayed for easy viewing and management of dialogue status.

## Example Interaction Flow

The following is a complete example flow demonstrating how to use Aisle to interact with AI:

1. **Set Dialogue Parameters**:

   ```python
   %panel --model qwen2.5:14b --temperature 0.7
   ```

2. **Send Message to AI**:

   ```python
   %%ai --image path/to/image.png --clear
   The weather is great today, do you have any suggestions?
   ```

3. **View Runtime Logs**: Switch to the "Logs" tab in the panel to view interaction records and system logs with AI.
