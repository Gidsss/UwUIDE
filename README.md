# UwU++

Automata Project for 3rd Year

## Get Started

1. Create a virtual environment `python -m venv .env`
2. Activate environment For CMD `./.env/Scripts/activate.bat` For bash `source ./.env/Scripts/activate`
3. Install dependencies using pip `python -m pip install -r requirements.txt`

## Unit Testing

1. For unit testing, we'll be using `pytest`.
2. To create a test file, simply follow these file formats: `test_*.py` or `*_test.py`
3. For more information, please refer to the official [Pytest documentation](https://docs.pytest.org/en/7.1.x/getting-started.html#)

## Running Tasks

1. Make sure you've installed the dependencies as we'll be using the `invoke` library for running tasks.
2. To run all tests, simply run this command: `invoke test`
3. To run a specific test file, simply run this command: `invoke test --file=< test file name >`
4. To run the idea, simply run this command: `invoke build`
