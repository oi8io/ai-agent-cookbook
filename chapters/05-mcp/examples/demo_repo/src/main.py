"""Minimal main module for demo purposes."""


def greet(name: str) -> str:
    """Return a greeting string.  TODO: add i18n support."""
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b


if __name__ == "__main__":
    print(greet("World"))
    print(f"1 + 2 = {add(1, 2)}")
