
# HubData Assignment

This repo contains details for the Datopian Assignment.

# Installation

This Project requires that you have Python 3.8.1 installed. If you do not have it installed, you can download it [here](https://www.python.org/downloads/release/python-381/).

## To Setup a Python 3  Virtual  Environment
After you have installed Python, you can run the following in your Terminal

```python3 -m venv /path/to/new/virtual/environment```

Example:

```python3 -m venv venv```

## Activate Virtual Environment

Run the following in your Command prompt /Terminal
### For Windows
```bash
source /path/to/new/virtual/environment/Scripts/activate
```
Example:
```bash
venv/Scripts/activate
```

### For Linux and MacOS
```bash
source /path/to/new/virtual/environment/Scripts/activate
```
Example:

```bash
source venv/Scripts/activate
```

### Install necessary Libraries

```bash
python3 -m pip install -r requirements.txt
```
**NOTE**:
To run the second scraper (scraper_2.py), you need to have Google Chrome installed as well as Chromedriver on your Machine.

# Usage

To use the project:

1. Clone the project to your local machine
2. Create a virtual environment, named `env`, with `python3 -m env /env` in project root
3. Activate the virtual environment with steps highlighted above
4. Run the scraper with any of the following options:

     Run the scraper using the default period: **day**

       python main.py

    Select based on a specific period [day, week, month, year]

       python main.py --period=year

    Save File with custom filename
       python main.py --period=year --filename=yearly_prices.csv



The results are stored as **{period}_{current_date}.csv** format
