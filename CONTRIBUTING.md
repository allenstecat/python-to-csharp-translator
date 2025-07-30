# Contributing to Python to C# Translator

🎉 Thank you for your interest in contributing to this project! We welcome contributions from everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## 📜 Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code:

- **Be respectful** and inclusive
- **Be collaborative** and constructive
- **Be patient** with newcomers
- **Focus on what's best** for the community

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Text editor or IDE
- Basic understanding of Python AST and C# syntax

### Development Setup

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/python-to-csharp-translator.git
   cd python-to-csharp-translator
   ```

3. **Set up upstream remote**
   ```bash
   git remote add upstream https://github.com/originalowner/python-to-csharp-translator.git
   ```

4. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

5. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt  # If we add any
   ```

## 🤝 How to Contribute

### 🐛 Reporting Bugs

1. **Check existing issues** first
2. **Use the bug report template**
3. **Include**:
   - Python version
   - Input Python code
   - Expected C# output
   - Actual output
   - Error messages

### 💡 Suggesting Features

1. **Check existing feature requests**
2. **Use the feature request template**
3. **Explain**:
   - Use case and motivation
   - Proposed implementation approach
   - Examples of the feature in action

### 🔧 Code Contributions

#### Areas for Contribution

1. **Language Features**
   - New AST node types
   - Advanced Python constructs
   - C# language feature mapping

2. **Improvements**
   - Better type inference
   - Smarter function mapping
   - Performance optimizations

3. **Documentation**
   - Code examples
   - Tutorial content
   - API documentation

4. **Testing**
   - Test cases for edge cases
   - Integration tests
   - Performance benchmarks

## 🔄 Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number-description
```

### 2. Make Changes

- **Write clear commit messages**
- **Keep commits focused** (one logical change per commit)
- **Test your changes**

### 3. Update Documentation

- Update README if needed
- Add/update code comments
- Update CHANGELOG.md

### 4. Submit Pull Request

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create pull request** on GitHub

3. **Fill out the PR template**

4. **Link related issues**

### 5. Code Review Process

- **All PRs need review** before merging
- **Address feedback** promptly
- **Update PR** as requested
- **Squash commits** if requested

## 📝 Coding Standards

### Python Code Style

```python
# Use descriptive names
def translate_function_definition(self, node):
    """Translate a Python function definition to C#."""
    pass

# Add type hints where helpful
def visit_expr(self, node: ast.expr) -> str:
    """Visit an expression node and return C# code."""
    pass

# Use docstrings for public methods
def translate_file(input_file: str, output_file: str = None) -> str:
    """
    Translate a Python file to C#.
    
    Args:
        input_file: Path to input Python file
        output_file: Optional output file path
        
    Returns:
        Generated C# code as string
    """
    pass
```

### AST Node Handling

```python
def visit_NewNodeType(self, node):
    """Handle new AST node type."""
    # Always check node attributes exist
    if hasattr(node, 'attribute'):
        value = node.attribute
    
    # Handle different node types gracefully
    if isinstance(node.target, ast.Name):
        name = node.target.id
    elif isinstance(node.target, ast.Attribute):
        name = f"{self.visit_expr(node.target.value)}.{node.target.attr}"
    
    return result
```

### C# Code Generation

```python
# Use consistent indentation
self.add_line("public class Example")
self.add_line("{")
self.indent_level += 1
self.add_line("// Class content")
self.indent_level -= 1
self.add_line("}")

# Generate clean, readable C#
def generate_method(self, name, params, body):
    """Generate clean C# method."""
    self.add_line(f"public void {name}({params})")
    self.add_line("{")
    self.indent_level += 1
    # ... method body
    self.indent_level -= 1
    self.add_line("}")
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_translator.py

# Run with coverage
python -m pytest tests/ --cov=py_to_cs_agent
```

### Writing Tests

```python
def test_function_translation():
    """Test basic function translation."""
    python_code = """
def greet(name):
    return f"Hello {name}"
    """
    
    expected_cs = """
public static string greet(string name)
{
    return $"Hello {name}";
}
    """.strip()
    
    result = translate_code(python_code)
    assert normalize_whitespace(result) == normalize_whitespace(expected_cs)
```

### Test Categories

1. **Unit Tests**: Individual AST node translation
2. **Integration Tests**: Complete file translation
3. **Edge Cases**: Error conditions and unusual inputs
4. **Performance Tests**: Large file handling

## 📚 Documentation

### Code Comments

```python
class PythonToCSharpTranslator(ast.NodeVisitor):
    """
    AST visitor that translates Python code to C# equivalents.
    
    This class walks through Python AST nodes and generates
    corresponding C# code using the visitor pattern.
    
    Attributes:
        output: List of generated C# code lines
        indent_level: Current indentation level
        function_mapping: Python to C# function name mapping
    """
```

### README Updates

- Keep examples current
- Update feature support table
- Add new CLI options
- Update installation instructions

## 🏷️ Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to docs
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `question` - Further information is requested

## 📞 Getting Help

- 💬 **GitHub Discussions** for questions
- 🐛 **GitHub Issues** for bugs
- 📧 **Direct contact** for sensitive issues

## 🎉 Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Added to contributors list

---

Thank you for contributing! 🚀
