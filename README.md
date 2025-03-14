# Witch: A (slightly) Smarter Which

Witch is a command-line utility that extends the functionality of the traditional `which` command. If the exact command is not found in your system's PATH, Witch provides fuzzy matching suggestions to help you locate similar commands, highlighting the differences with ANSI color codes.

## Features

- **Exact Match Search:** Quickly locate the full path of an executable using `shutil.which()`.
- **Fuzzy Matching:** If the command is not found, Witch suggests close matches based on your input.

## Requirements

- Python 3.x
- [wcwidth](https://pypi.org/project/wcwidth/)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/witch.git
   cd witch
   ```

2. **Install Dependencies:**

   Use `pip` to install the required package:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run Witch from the command line by providing the command you want to search for as an argument:

```bash
python witch.py <command>
```

### Example

If you search for a non-existent command:

```bash
python witch.py wwichj
```

Witch might output:

```
Command not found. Did you mean:

Suggested Command    | Location
-------------------------------------------------------------------------
witch                            | /home/USER/.local/bin/witch
which                            | /usr/bin/which
watch                            | /usr/bin/watch


```

This output helps you identify a close match with highlighted differences, making it easier to spot potential typos or variations.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```