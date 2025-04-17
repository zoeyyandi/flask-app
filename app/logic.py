def add(a, b):
    return float(a) + float(b)

def subtract(a, b):
    return float(a) - float(b)

def multiply(a, b):
    return float(a) * float(b)

def square(a):
    return float(a) ** 2

def divide(a, b):
    if float(b) == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return float(a) / float(b)
