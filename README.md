<div align="center">

# NFL Fantaspy

Scrape team and game history data from your NFL fantasy football league. Archive the data as a JSON file or automatically upload to your Airtable account.

[Installation](#installation) •
[Getting started](#getting-started) •
[Configuration](#configuration) •
[Limitations](#limitations) 
</div>

## Installation
### Step 1: Have Python3.9+ installed
Python3.9+ is the recommended version to run NFLFantaspy. Older versions of Python have not been tested.

### Step 2: Clone the repository
Example clone using SSH.
```bash
git clone git@github.com:mpanelo/nflfantaspy.git
```

### Step 3: Create a virtual environment
Use a virtual environment to avoid dependency collisions.
```bash
cd nflfantaspy 
```
```bash
python3.9 -m venv venv
```
```bash
source venv/bin/activate
```

### Step 4: Install the package
NFLFantaspy is a pip installable package (not yet published on PyPI). Go inside the root directory, and install using pip.
```bash
pip install .
```

## Getting Started
To run the command, make sure you've activated the virutal environment and installed the package.

### Examples:
Scrape game history from the years 2014-2021. The scraped data will be stored to JSON.
```bash
python -m nflfantaspy json --league-id=LEAGUE_ID --data-type=games --years=2014-2021
```

Scrape team history data just for 2018. Store the data on Airtable.
```bash
python -m nflfantaspy airtable \
    --league-id=LEAGUE_ID \
    --data-type=teams \
    --years=2018 \
    --api-key=AIRTABLE_API_KEY \
    --base-id=AIRTABLE_BASE_ID
```

## Configuration
Before using the Airtable storage option, make sure you've configured your Airtable account:
### Step 1: Generate API Key
Go to your [account page](https://airtable.com/account) and generate your personal API key.

### Step 2: Create a Base For Each Data Type You Intend to Scrape
For example, if you're going to scrape games history data. Create a Base for games, and a table for every year you're planning to scrape.

The current Airtable API does not support dynamic Base and Table creation.

## Feedback