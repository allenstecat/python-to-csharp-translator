# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-30

### Added
- 🎉 Initial release of Python to C# Translator
- AST-based translation with visitor pattern
- Support for classes, methods, and inheritance
- Control flow translation (if/else, while, for loops)
- Exception handling (try-catch-finally)
- LINQ integration for list comprehensions
- String interpolation (f-strings to $-strings)  
- Smart function/method/exception mapping
- Type annotation conversion
- CLI interface with argparse
- Comprehensive documentation
- MIT License

### Features
- **Classes**: Full class definition support with inheritance
- **Methods**: Instance and static method translation
- **Control Flow**: if/else, while, for loops with range() support
- **Exceptions**: try-except-finally → try-catch-finally
- **Collections**: List, dict, set literals and operations
- **Comprehensions**: List/dict/set comprehensions → LINQ
- **Built-ins**: print(), len(), sum(), range(), etc.
- **Operators**: Binary, unary, comparison operators
- **Types**: Type annotation mapping and inference

### Technical Details
- Uses Python 3.7+ AST module
- No external dependencies
- Generates .NET 5.0+ compatible C# code
- Visitor pattern for extensible AST processing
- Smart type inference and mapping
- LINQ expressions for functional operations

### Documentation
- Complete README with examples
- API documentation
- Development guide
- Contributing guidelines
- Code examples and test cases

## [Unreleased]

### Planned Features
- [ ] Enhanced type inference
- [ ] Async/await support
- [ ] Decorator translation
- [ ] Package structure mapping
- [ ] Unit test translation
- [ ] Documentation comment conversion
