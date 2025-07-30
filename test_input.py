#!/usr/bin/env python3
"""
Test Python file for translation to C#
"""

class Calculator:
    def __init__(self, name: str):
        self.name = name
        self.history = []
    
    def add(self, a: int, b: int) -> int:
        result = a + b
        self.history.append(f"Added {a} + {b} = {result}")
        return result
    
    def process_numbers(self, numbers: list) -> list:
        # List comprehension example
        return [x * 2 for x in numbers if x > 0]
    
    def get_stats(self, data: list) -> dict:
        return {
            'sum': sum(data),
            'max': max(data),
            'count': len(data)
        }

def main():
    calc = Calculator("MyCalc")
    
    # Basic operations
    result = calc.add(5, 3)
    print(f"Result: {result}")
    
    # List processing
    numbers = [1, -2, 3, -4, 5]
    processed = calc.process_numbers(numbers)
    print(f"Processed: {processed}")
    
    # Statistics
    stats = calc.get_stats([1, 2, 3, 4, 5])
    print(f"Stats: {stats}")
    
    # Exception handling
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    
    # Loops
    for i in range(3):
        print(f"Loop {i}")

if __name__ == "__main__":
    main()
