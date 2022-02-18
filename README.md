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
Python3.9+ is the recommended version to run NFLFantaspy. I have not tested older versions of Python.

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
Scrape game history for the years 2014-2021, and store it as JSON.
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
The current Airtable API does not support dynamic Base and Table creation.

You will need to create a Base for each supported data-type and Tables for each year. For example, if you're going to scrape game history for the years 2014-2016 and 2021, then create the following:
<img width="1512" alt="Screen Shot 2022-02-16 at 8 40 30 PM" src="https://user-images.githubusercontent.com/17281354/154620254-45b0c2b1-a6e9-4923-b2ab-efcf8d6022f1.png">

### Step 3: Create the Table fields
Dynamic creation of Table fields is also not supported. Create the following fields for your Tables in the Games Base:

| Field Name  | Type |
| ------------| -------------|
| id          | Number (Integer) |
| home_id     | Number (Integer) |
| away_id     | Number (Integer) |
| home_score  | Number (Decimal, 1.00 Precision) |
| away_score  | Number (Decimal, 1.00 Precision) |
| type        | Single select (Options: REGULAR, PLAYOFF, CONSOLATION) |

Create the following fields for your Tables in the Teams Base:
| Field Name  | Type |
| ------------| -------------|
| id          | Number (Integer) |
| name        | Single line text |
| owner        | Single line text |

### Step 4: Get the Base IDs
Get the Base ID from the [URL](https://support.airtable.com/hc/en-us/articles/4405741487383-Understanding-Airtable-IDs) or click on the Base in the [API docs](https://airtable.com/api).

## Limitations
- Storing data to Airtable requires manual configuration
- Your NFL fantasy football league needs to be Public (NFL API is not open to the public)
- Project is not 100% complete
  - There are still enhancements left to do to make the DX better
  - Bugs left to resolve

## Feedback
I appreciate all feedback! To get in contact, send me a DM on [Twitter](https://twitter.com/maupanelo).
