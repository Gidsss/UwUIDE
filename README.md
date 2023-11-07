# UwU++

Automata Project for 3rd Year

## Get Started

1. Create a virtual environment `python -m venv .env`
2. Activate environment For CMD `.\venv\scripts\activate` For bash `source ./.env/Scripts/activate`
3. Install dependencies using pip `python -m pip install -r requirements.txt`

## Unit Testing

1. For unit testing, we'll be using `pytest`
2. To create a test file, simply follow these file formats: `test_*.py` or `*_test.py`
3. For more information, please refer to the official [Pytest documentation](https://docs.pytest.org/en/7.1.x/getting-started.html#)

## UwU Console Script Package

1. Install the UwU Console Script Package `python -m pip install ./packages/uwu`

2. To install | uninstall packages from `requirements.txt`

```bash
uwu install
uwu uninstall
```

3. To install | uninstall individual packages

```bash
uwu install < package name >
uwu uninstall < package name >
```

4. To run all tests `uwu test`
5. To run a specific test

```bash
uwu test test_*
uwu test *_test
```

6. To run lexer package `uwu lexer`

7. To build UwU IDE `uwu build`
