# Python to C# Translator

🔄 **Automatic Python to C# code translator using AST parsing**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![C# .NET](https://img.shields.io/badge/.NET-5.0+-purple.svg)](https://dotnet.microsoft.com/)

Transform your Python code into equivalent C# code automatically! This tool uses Abstract Syntax Tree (AST) parsing to provide accurate, maintainable translations with comprehensive language feature support.

## ✨ Features

- 🔧 **AST-Based Translation**: Uses Python's AST module for accurate parsing
- 🏗️ **Comprehensive Language Support**: Classes, methods, control flow, exceptions
- 🔗 **LINQ Integration**: Python list comprehensions → C# LINQ expressions  
- 🎯 **Smart Mapping**: Intelligent function/method/exception type mapping
- 💬 **String Interpolation**: f-strings automatically convert to C# $-strings
- 📝 **Type Annotations**: Python type hints → C# strong typing
- 🖥️ **CLI Interface**: Simple command-line operation with file I/O
- 📚 **No Dependencies**: Uses only Python standard library

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/yourusername/python-to-csharp-translator.git
cd python-to-csharp-translator
```

### Basic Usage

```bash
# Translate a Python file to C#
python py_to_cs_agent.py input.py output.cs

# Print to console
python py_to_cs_agent.py input.py

# Verbose output
python py_to_cs_agent.py input.py output.cs --verbose
```

## 📋 Language Support

### ✅ Supported Features

| Python Feature | C# Translation | Example |
|---------------|----------------|---------|
| Classes | Classes with inheritance | `class User(BaseUser):` → `public class User : BaseUser` |
| Methods | Instance/static methods | `def calculate(self, x):` → `public object calculate(object x)` |
| Control Flow | if/else, while, for loops | `for i in range(10):` → `for (int i = 0; i < 10; i++)` |
| Exceptions | try-catch-finally | `except ValueError:` → `catch (ArgumentException)` |
| Comprehensions | LINQ expressions | `[x*2 for x in nums]` → `nums.Select(x => x*2).ToList()` |
| f-strings | String interpolation | `f"Hello {name}"` → `$"Hello {name}"` |
| Built-ins | Standard library mapping | `len(items)` → `items.Count` |

### 🔄 Translation Examples

**Python Input:**
```python
class Calculator:
    def __init__(self, name: str):
        self.name = name
    
    def add_numbers(self, nums: list) -> int:
        return sum(nums)
    
    def process_data(self, data: list) -> list:
        return [x * 2 for x in data if x > 0]

# Usage
calc = Calculator("MyCalc")
result = calc.add_numbers([1, 2, 3, 4, 5])
filtered = calc.process_data([-1, 2, -3, 4])
print(f"Result: {result}")
```

**C# Output:**
```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;

namespace PythonTranslated
{
    public class Calculator
    {
        public Calculator(string name)
        {
            var name = name;
        }
        
        public int add_numbers(List nums)
        {
            return nums.Sum();
        }
        
        public List process_data(List data)
        {
            return data.Where(x => x > 0).Select(x => x * 2).ToList();
        }
    }
    
    public class Program
    {
        public static void Main()
        {
            var calc = new Calculator("MyCalc");
            var result = calc.add_numbers(new List<object> {1, 2, 3, 4, 5});
            var filtered = calc.process_data(new List<object> {-1, 2, -3, 4});
            Console.WriteLine($"Result: {result}");
        }
    }
}
```

## 🛠️ Advanced Usage

### Command Line Options

```bash
python py_to_cs_agent.py --help

# Options:
#   input_file        Input Python file (.py)
#   output_file       Output C# file (.cs) - optional  
#   -v, --verbose     Enable verbose output
```

### Python API

```python
from py_to_cs_agent import translate_file

# Translate file
csharp_code = translate_file('input.py', 'output.cs')

# Get translation as string
csharp_code = translate_file('input.py')
```

## 🎯 Translation Mapping

### Function Mapping
- `print()` → `Console.WriteLine()`
- `len()` → `.Count` property
- `range()` → `Enumerable.Range()`
- `sum()` → `.Sum()` LINQ method

### Exception Mapping  
- `ValueError` → `ArgumentException`
- `KeyError` → `KeyNotFoundException`
- `IndexError` → `IndexOutOfRangeException`
- `FileNotFoundError` → `FileNotFoundException`

### Collection Operations
- `list.append()` → `List.Add()`
- `dict.keys()` → `Dictionary.Keys`
- `str.split()` → `string.Split()`
- `[x for x in items]` → `items.Select(x => x).ToList()`

## 📁 Project Structure

```
python-to-csharp-translator/
├── py_to_cs_agent.py          # Main translator script
├── README.md                  # This file
├── LICENSE                    # MIT License
├── CONTRIBUTING.md            # Contribution guidelines
├── CHANGELOG.md               # Version history
├── examples/                  # Example translations
│   ├── basic_example.py
│   ├── basic_example.cs
│   ├── advanced_example.py
│   └── advanced_example.cs
└── docs/                      # Documentation
    ├── API_DOCUMENTATION.md
    ├── DEVELOPMENT_GUIDE.md
    └── EXAMPLES.md
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
git clone https://github.com/yourusername/python-to-csharp-translator.git
cd python-to-csharp-translator

# Run tests
python -m pytest tests/

# Format code
black py_to_cs_agent.py

# Type checking
mypy py_to_cs_agent.py
```

## 📈 Roadmap

- [ ] **Enhanced Type Inference**: Better automatic type detection
- [ ] **Async/Await Support**: Python asyncio → C# async/await
- [ ] **Decorator Translation**: Python decorators → C# attributes
- [ ] **Package Structure**: Python modules → C# namespaces
- [ ] **Unit Test Translation**: pytest → NUnit/xUnit
- [ ] **Documentation Comments**: Python docstrings → C# XML docs

## ⚠️ Limitations

- **Manual Review Required**: Generated code should be reviewed and tested
- **Complex Expressions**: Some advanced Python features may need manual adjustment
- **Third-Party Libraries**: Library-specific code requires manual porting
- **Dynamic Features**: Python's dynamic nature doesn't always translate directly

## 🔧 Requirements

- **Python**: 3.7 or higher
- **Dependencies**: None (uses only standard library)
- **Output**: Compatible with .NET 5.0+ and .NET Framework 4.7+

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Python AST documentation and examples
- .NET and C# language specifications  
- LINQ documentation and best practices
- Open source contributors and feedback

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/python-to-csharp-translator/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/yourusername/python-to-csharp-translator/discussions)
- 📧 **Contact**: [Your contact information]

---

⭐ **Star this repository if you find it helpful!**

🔄 **Transform your Python code to C# today!**
