# Python custom agent using Gemini 

This is a simple command-line calculator application that evaluates mathematical expressions.

## How to Run

To run the calculator, execute the `main.py` file with your desired expression as an argument:

```bash
uv run main.py "Find the bug in the calculator app: 3 + 7 * 2 shouldn't be 20"
```

Application will print function calls and final response of the model 

## Sample tests

```bash
uv run main.py "create a new README.md file with the contents '# calculator'" --verbose
```

```bash
uv run main.py "get the contents of lorem.txt" --verbose
```

```bash
uv run main.py "run tests.py" --verbose
```

```bash
uv run main.py "what files are in the root?" --verbose
```
