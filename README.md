# API Test

This repository contains test functions written in Python (using pytest framework) to validate the functionality and data consistency of the Pokemon API (`https://pokeapi.co/api/v2/`).

## Requirements
- Python 3.x
- pytest
- requests

## Installation
### 1. Clone the repository:
```bash
git clone https://github.com/shachar08/API_Test
```

### 2. Install dependencies:
```bash
pip install requests
pip install pytest
```

## Test Functions Overview

### test_section_1
verify that there are exactly 20 different pokemon types.

### test_section_2
finds the ID of the "Fire type" and verify that the pokemon "charmander" is from type Fire and that the pokemon "bulbasaur" is not

### test_section_3
finds the five heaviest pokemons and their weights, and checks if the result is matching what we expected

## Running Tests
To execute the test suite, run the following command:
```bash
pytest -v
```
