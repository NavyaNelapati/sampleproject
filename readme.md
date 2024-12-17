
# Sample Booking Management Test Project

## Overview
This project is a sample implementation of a test automation suite for managing bookings using a BDD (Behavior-Driven Development) approach. The tests interact with a booking API and verify functionalities like creating, reading, updating, and deleting bookings. This suite uses tools such as `pytest`, `pytest-bdd`

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Configuration](#configuration)
- [Generating Test Data](#generating-test-data)
- [Reports](#reports)

## Features
- **Booking Management**: Create, read, update, and delete booking scenarios.
- **Behavior-Driven Development (BDD)**: Gherkin-style feature files to describe scenarios.
- **Automated Testing**: Uses `pytest` for testing, with structured step definitions.
- **Configurable Test Data**: Easily manage test data through JSON files.
- **Reports**: HTML-based test reports to visualize the results.


## Project Structure
```
.
├── generate_testdata.py          # Script for generating test data
├── pyproject.toml                # Project and build configuration
├── pytest.ini                    # pytest configuration file
├── requirements.txt              # Dependencies for the project
├── tests
│   ├── features                  # BDD feature files (Gherkin syntax)
│   │   ├── createBooking.feature
│   │   ├── deleteBooking.feature
│   │   ├── readBooking.feature
│   │   └── updateBooking.feature
│   ├── resources
│   │   └── testdata.json         # JSON file containing test data
│   ├── steps                     # Step definitions for feature files
│   │   ├── test_createbooking.py
│   │   ├── test_deleteBooking.py
│   │   ├── test_readbooking.py
│   │   └── test_updatebooking.py
│   ├── utils.py                  # Utility functions used across tests
│   ├── constants.py              # Constants used in test scripts
│   ├── conftest.py               # Shared test configurations and fixtures
│   └── __init__.py
└── reports
    ├── samplereport.html         # Sample report for test runs
```

## Installation

To run the tests locally, make sure you have Python 3.8 or above installed.

1. create virtual env and activate it
    On MacOS/Linux:

        python3 -m venv .venv
        source .venv/bin/activate

    On Windows: 

        python3 -m venv .venv
        .venv\Scripts\activate

2. Install the project dependencies from the `requirements.txt` file using `pip`:
       
        pip install -r requirements.txt

## Generating Test Data
    
    Use the provided `generate_testdata.py` script to create or modify test data.

        python generate_testdata.py

    NOTE: Please ensure to set up the test data each time before executing the test cases, as certain scenarios, like "Delete Booking," may fail if the records from the initial test data have already been deleted.


## Usage

- **Feature Files**: Located in `tests/features/`. Describe the expected behavior of booking functionalities.
- **Step Definitions**: Located in `tests/steps/`. These contain the actual code to automate the steps defined in the feature files.
- **Test Data**: Test data is maintained in `tests/resources/testdata.json`.

## Running Tests
To run the test suite, use the following command:

```sh
pytest tests/ --gherkin-terminal-reporter --bdd-report=reports/samplereport.html --tb=short
```
- **Options**:
  - `--gherkin-terminal-reporter`: Shows BDD-style output in the terminal.
  - `--bdd-report=reports/samplereport.html`: Generates an HTML report with the test results.
  - `--tb=short`:    shorter traceback format
  - `--log-cli-level WARN`:  logging level for test scenarios

 To execute tests without generating report
    `pytest tests/ --tb=short`

### Running Tests using tags(individual features)

```sh
pytest tests/ -m "readBooking" --gherkin-terminal-reporter --bdd-report=reports/samplereport.html --tb=short
```

## Reports
Test reports are generated in the HTML format after running the tests with the `--bdd-report` flag. You can find the reports in the `reports/` directory

To execute tests along with generating report

`pytest tests/ --tb=short --bdd-report=reports/{report_name}.html`

Ex: `pytest tests --tb=short --bdd-report=reports/samplereport.html`

## Quick Summary of Bugs identified

createBooking.feature:
1. A booking should not be created if the check-in date is later than the check-out date, but the system is allowing such bookings.

updateBooking.feature:
2. A booking should not be updated if it has already expired, but the system is allowing updates to expired bookings.
3. A partial update should not be allowed for an expired booking, but the system is permitting partial updates to expired bookings.

readBooking.feature:
1. When an invalid checkout date is provided, no records should be returned. However, the response is 200, and records are being returned.
2. If an invalid checkout date format (not in YYYY-MM-DD format, e.g., 01-01-2020) is passed, no records should be returned. Instead, a 200 response is received, and records are being returned.

Another observation: The returned status codes seem to be inconsistent and not appropriately chosen. For example, deleting a non-existing booking returns a 405, while a successful deletion of a booking returns a 201.