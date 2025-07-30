#!/usr/bin/env python3
"""
Python to C# Code Translator
============================

A comprehensive AST-based translator that converts Python code to C# equivalents.
Supports classes, methods, control flow, exceptions, comprehensions, and more.

Usage:
    python py_to_cs_agent.py input_file.py [output_file.cs]

Features:
- AST-based parsing with visitor pattern
- Smart function/method/exception mapping
- LINQ integration for comprehensions
- Type annotation conversion
- String interpolation (f-strings to $-strings)
- CLI interface with file I/O
"""

import ast
import argparse
import sys
import os


class PythonToCSharpTranslator(ast.NodeVisitor):
    """AST visitor that translates Python code to C# equivalents."""
    
    def __init__(self):
        self.output = []
        self.indent_level = 0
        self.in_class = False
        self.current_class = None
        
        # Function mapping from Python to C#
        self.function_mapping = {
            'print': 'Console.WriteLine',
            'len': 'Count',  # For collections
            'str': 'ToString',
            'int': 'int.Parse',
            'float': 'double.Parse',
            'bool': 'bool.Parse',
            'range': 'Enumerable.Range',
            'sum': 'Sum',  # LINQ method
            'max': 'Max',  # LINQ method
            'min': 'Min',  # LINQ method
            'sorted': 'OrderBy',  # LINQ method
            'reversed': 'Reverse',  # LINQ method
            'enumerate': 'Select',  # LINQ with index
            'zip': 'Zip',  # LINQ method
            'filter': 'Where',  # LINQ method
            'map': 'Select',  # LINQ method
            'any': 'Any',  # LINQ method
            'all': 'All',  # LINQ method
        }
        
        # Method mapping (when called on objects)
        self.method_mapping = {
            'append': 'Add',
            'extend': 'AddRange',
            'insert': 'Insert',
            'remove': 'Remove',
            'pop': 'RemoveAt',
            'clear': 'Clear',
            'sort': 'Sort',
            'reverse': 'Reverse',
            'index': 'IndexOf',
            'count': 'Count',
            'split': 'Split',
            'join': 'Join',
            'strip': 'Trim',
            'lower': 'ToLower',
            'upper': 'ToUpper',
            'replace': 'Replace',
            'startswith': 'StartsWith',
            'endswith': 'EndsWith',
            'find': 'IndexOf',
            'keys': 'Keys',
            'values': 'Values',
            'items': 'ToList',  # For dictionary iteration
        }
        
        # Exception mapping
        self.exception_mapping = {
            'Exception': 'Exception',
            'ValueError': 'ArgumentException',
            'TypeError': 'InvalidOperationException',
            'KeyError': 'KeyNotFoundException',
            'IndexError': 'IndexOutOfRangeException',
            'FileNotFoundError': 'FileNotFoundException',
            'IOError': 'IOException',
            'RuntimeError': 'SystemException',
            'NotImplementedError': 'NotImplementedException',
            'AttributeError': 'MemberAccessException',
        }
        
        # Type mapping
        self.type_mapping = {
            'int': 'int',
            'float': 'double',
            'str': 'string',
            'bool': 'bool',
            'list': 'List',
            'dict': 'Dictionary',
            'set': 'HashSet',
            'tuple': 'Tuple',
            'None': 'null',
            'True': 'true',
            'False': 'false',
        }

    def indent(self):
        """Return current indentation string."""
        return "    " * self.indent_level

    def add_line(self, line=""):
        """Add a line with proper indentation."""
        if line:
            self.output.append(self.indent() + line)
        else:
            self.output.append("")

    def visit_Module(self, node):
        """Handle module-level code."""
        self.add_line("using System;")
        self.add_line("using System.Collections.Generic;")
        self.add_line("using System.Linq;")
        self.add_line("using System.IO;")
        self.add_line()
        
        self.add_line("namespace PythonTranslated")
        self.add_line("{")
        self.indent_level += 1
        
        # Check if we need a main class for standalone functions
        has_functions = any(isinstance(child, ast.FunctionDef) for child in node.body)
        has_classes = any(isinstance(child, ast.ClassDef) for child in node.body)
        
        if has_functions and not has_classes:
            self.add_line("public class Program")
            self.add_line("{")
            self.indent_level += 1
        
        for child in node.body:
            self.visit(child)
        
        if has_functions and not has_classes:
            self.indent_level -= 1
            self.add_line("}")
        
        self.indent_level -= 1
        self.add_line("}")

    def visit_ClassDef(self, node):
        """Handle class definitions."""
        self.add_line()
        
        # Handle inheritance
        bases = ""
        if node.bases:
            base_names = [self.visit_expr(base) for base in node.bases]
            bases = f" : {', '.join(base_names)}"
        
        self.add_line(f"public class {node.name}{bases}")
        self.add_line("{")
        self.indent_level += 1
        self.in_class = True
        self.current_class = node.name
        
        for child in node.body:
            self.visit(child)
        
        self.in_class = False
        self.current_class = None
        self.indent_level -= 1
        self.add_line("}")

    def visit_FunctionDef(self, node):
        """Handle function definitions."""
        self.add_line()
        
        # Handle constructor
        if self.in_class and node.name == "__init__":
            params = self.get_parameters(node.args)
            self.add_line(f"public {self.current_class}({params})")
        else:
            # Determine access modifier
            access = "public" if self.in_class else "public static"
            
            # Handle return type (simplified)
            return_type = "void"
            if node.returns:
                return_type = self.get_type_annotation(node.returns)
            
            params = self.get_parameters(node.args)
            self.add_line(f"{access} {return_type} {node.name}({params})")
        
        self.add_line("{")
        self.indent_level += 1
        
        for child in node.body:
            self.visit(child)
        
        self.indent_level -= 1
        self.add_line("}")

    def get_parameters(self, args):
        """Extract function parameters."""
        params = []
        for arg in args.args:
            param_type = "object"  # Default type
            if arg.annotation:
                param_type = self.get_type_annotation(arg.annotation)
            params.append(f"{param_type} {arg.arg}")
        return ", ".join(params)

    def get_type_annotation(self, annotation):
        """Convert Python type annotation to C# type."""
        if isinstance(annotation, ast.Name):
            return self.type_mapping.get(annotation.id, annotation.id)
        elif isinstance(annotation, ast.Constant):
            return str(annotation.value)
        return "object"

    def visit_Return(self, node):
        """Handle return statements."""
        if node.value:
            value = self.visit_expr(node.value)
            self.add_line(f"return {value};")
        else:
            self.add_line("return;")

    def visit_Assign(self, node):
        """Handle variable assignments."""
        if len(node.targets) == 1:
            target = node.targets[0]
            value = self.visit_expr(node.value)
            
            if isinstance(target, ast.Name):
                # Simple variable assignment
                var_type = self.infer_type(node.value)
                self.add_line(f"{var_type} {target.id} = {value};")
            elif isinstance(target, ast.Attribute):
                # Attribute assignment
                obj = self.visit_expr(target.value)
                self.add_line(f"{obj}.{target.attr} = {value};")
            elif isinstance(target, ast.Subscript):
                # Subscript assignment
                obj = self.visit_expr(target.value)
                index = self.visit_expr(target.slice)
                self.add_line(f"{obj}[{index}] = {value};")

    def visit_AnnAssign(self, node):
        """Handle annotated assignments (type hints)."""
        if node.target and isinstance(node.target, ast.Name):
            var_type = self.get_type_annotation(node.annotation)
            var_name = node.target.id
            
            if node.value:
                value = self.visit_expr(node.value)
                self.add_line(f"{var_type} {var_name} = {value};")
            else:
                self.add_line(f"{var_type} {var_name};")

    def visit_AugAssign(self, node):
        """Handle augmented assignments (+=, -=, etc.)."""
        target = self.visit_expr(node.target)
        value = self.visit_expr(node.value)
        op = self.get_operator(node.op)
        self.add_line(f"{target} {op}= {value};")

    def visit_If(self, node):
        """Handle if statements."""
        condition = self.visit_expr(node.test)
        self.add_line(f"if ({condition})")
        self.add_line("{")
        self.indent_level += 1
        
        for child in node.body:
            self.visit(child)
        
        self.indent_level -= 1
        self.add_line("}")
        
        # Handle elif/else
        if node.orelse:
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                # elif case
                self.add_line("else")
                self.visit(node.orelse[0])
            else:
                # else case
                self.add_line("else")
                self.add_line("{")
                self.indent_level += 1
                
                for child in node.orelse:
                    self.visit(child)
                
                self.indent_level -= 1
                self.add_line("}")

    def visit_While(self, node):
        """Handle while loops."""
        condition = self.visit_expr(node.test)
        self.add_line(f"while ({condition})")
        self.add_line("{")
        self.indent_level += 1
        
        for child in node.body:
            self.visit(child)
        
        self.indent_level -= 1
        self.add_line("}")

    def visit_For(self, node):
        """Handle for loops."""
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name):
            if node.iter.func.id == "range":
                # Handle range() loops
                args = node.iter.args
                target_name = node.target.id if isinstance(node.target, ast.Name) else "i"
                
                if len(args) == 1:
                    # range(n)
                    end = self.visit_expr(args[0])
                    self.add_line(f"for (int {target_name} = 0; {target_name} < {end}; {target_name}++)")
                elif len(args) == 2:
                    # range(start, end)
                    start = self.visit_expr(args[0])
                    end = self.visit_expr(args[1])
                    self.add_line(f"for (int {target_name} = {start}; {target_name} < {end}; {target_name}++)")
                elif len(args) == 3:
                    # range(start, end, step)
                    start = self.visit_expr(args[0])
                    end = self.visit_expr(args[1])
                    step = self.visit_expr(args[2])
                    self.add_line(f"for (int {target_name} = {start}; {target_name} < {end}; {target_name} += {step})")
        else:
            # Handle foreach loops
            iterable = self.visit_expr(node.iter)
            var_type = "var"  # Use var for type inference
            target_name = node.target.id if isinstance(node.target, ast.Name) else "item"
            self.add_line(f"foreach ({var_type} {target_name} in {iterable})")
        
        self.add_line("{")
        self.indent_level += 1
        
        for child in node.body:
            self.visit(child)
        
        self.indent_level -= 1
        self.add_line("}")

    def visit_Break(self, node):
        """Handle break statements."""
        self.add_line("break;")

    def visit_Continue(self, node):
        """Handle continue statements."""
        self.add_line("continue;")

    def visit_Try(self, node):
        """Handle try-except blocks."""
        self.add_line("try")
        self.add_line("{")
        self.indent_level += 1
        
        for child in node.body:
            self.visit(child)
        
        self.indent_level -= 1
        self.add_line("}")
        
        # Handle except clauses
        for handler in node.handlers:
            self.visit_ExceptHandler(handler)
        
        # Handle finally
        if node.finalbody:
            self.add_line("finally")
            self.add_line("{")
            self.indent_level += 1
            
            for child in node.finalbody:
                self.visit(child)
            
            self.indent_level -= 1
            self.add_line("}")

    def visit_ExceptHandler(self, node):
        """Handle except clauses."""
        if node.type:
            exception_type = self.visit_expr(node.type)
            exception_type = self.exception_mapping.get(exception_type, exception_type)
            
            if node.name:
                self.add_line(f"catch ({exception_type} {node.name})")
            else:
                self.add_line(f"catch ({exception_type})")
        else:
            self.add_line("catch (Exception)")
        
        self.add_line("{")
        self.indent_level += 1
        
        for child in node.body:
            self.visit(child)
        
        self.indent_level -= 1
        self.add_line("}")

    def visit_Raise(self, node):
        """Handle raise statements."""
        if node.exc:
            exception = self.visit_expr(node.exc)
            self.add_line(f"throw new {exception};")
        else:
            self.add_line("throw;")

    def visit_Import(self, node):
        """Handle import statements."""
        # Most Python imports don't have direct C# equivalents
        # Add as comments for reference
        for alias in node.names:
            self.add_line(f"// import {alias.name}")

    def visit_ImportFrom(self, node):
        """Handle from...import statements."""
        # Add as comments for reference
        if node.module:
            for alias in node.names:
                self.add_line(f"// from {node.module} import {alias.name}")

    def visit_Expr(self, node):
        """Handle expression statements."""
        expr = self.visit_expr(node.value)
        self.add_line(f"{expr};")

    def visit_Pass(self, node):
        """Handle pass statements."""
        self.add_line("// pass")

    def visit_ListComp(self, node):
        """Handle list comprehensions using LINQ."""
        # [expr for target in iter if condition]
        # becomes: iter.Where(condition).Select(target => expr)
        
        iter_expr = self.visit_expr(node.generators[0].iter)
        target = node.generators[0].target.id if isinstance(node.generators[0].target, ast.Name) else "x"
        element_expr = self.visit_expr(node.elt)
        
        result = f"{iter_expr}.Select({target} => {element_expr})"
        
        # Handle conditions
        for generator in node.generators:
            for if_clause in generator.ifs:
                condition = self.visit_expr(if_clause)
                result = f"{iter_expr}.Where({target} => {condition}).Select({target} => {element_expr})"
        
        return result + ".ToList()"

    def visit_DictComp(self, node):
        """Handle dictionary comprehensions."""
        # {key: value for target in iter}
        # becomes: iter.ToDictionary(target => key, target => value)
        
        iter_expr = self.visit_expr(node.generators[0].iter)
        target = node.generators[0].target.id if isinstance(node.generators[0].target, ast.Name) else "x"
        key_expr = self.visit_expr(node.key)
        value_expr = self.visit_expr(node.value)
        
        return f"{iter_expr}.ToDictionary({target} => {key_expr}, {target} => {value_expr})"

    def visit_SetComp(self, node):
        """Handle set comprehensions."""
        # {expr for target in iter}
        # becomes: new HashSet<T>(iter.Select(target => expr))
        
        iter_expr = self.visit_expr(node.generators[0].iter)
        target = node.generators[0].target.id if isinstance(node.generators[0].target, ast.Name) else "x"
        element_expr = self.visit_expr(node.elt)
        
        return f"new HashSet<object>({iter_expr}.Select({target} => {element_expr}))"

    def visit_UnaryOp(self, node):
        """Handle unary operations."""
        operand = self.visit_expr(node.operand)
        op = self.get_unary_operator(node.op)
        return f"{op}{operand}"

    def visit_Tuple(self, node):
        """Handle tuple creation and unpacking."""
        if len(node.elts) <= 8:  # C# Tuple limit
            elements = [self.visit_expr(elt) for elt in node.elts]
            return f"({', '.join(elements)})"
        else:
            # Use array for large tuples
            elements = [self.visit_expr(elt) for elt in node.elts]
            return f"new object[] {{{', '.join(elements)}}}"

    def visit_expr(self, node):
        """Visit an expression node and return the C# equivalent."""
        if isinstance(node, ast.Constant):
            return self.visit_Constant(node)
        elif isinstance(node, ast.Name):
            return self.visit_Name(node)
        elif isinstance(node, ast.BinOp):
            return self.visit_BinOp(node)
        elif isinstance(node, ast.UnaryOp):
            return self.visit_UnaryOp(node)
        elif isinstance(node, ast.Compare):
            return self.visit_Compare(node)
        elif isinstance(node, ast.Call):
            return self.visit_Call(node)
        elif isinstance(node, ast.Attribute):
            return self.visit_Attribute(node)
        elif isinstance(node, ast.Subscript):
            return self.visit_Subscript(node)
        elif isinstance(node, ast.List):
            return self.visit_List(node)
        elif isinstance(node, ast.Dict):
            return self.visit_Dict(node)
        elif isinstance(node, ast.Set):
            return self.visit_Set(node)
        elif isinstance(node, ast.Tuple):
            return self.visit_Tuple(node)
        elif isinstance(node, ast.ListComp):
            return self.visit_ListComp(node)
        elif isinstance(node, ast.DictComp):
            return self.visit_DictComp(node)
        elif isinstance(node, ast.SetComp):
            return self.visit_SetComp(node)
        elif isinstance(node, ast.BoolOp):
            return self.visit_BoolOp(node)
        elif isinstance(node, ast.JoinedStr):
            return self.visit_JoinedStr(node)
        elif isinstance(node, ast.FormattedValue):
            return self.visit_FormattedValue(node)
        else:
            return f"/* Unsupported expression: {type(node).__name__} */"

    def visit_Constant(self, node):
        """Handle constant values."""
        value = node.value
        if isinstance(value, str):
            # Escape quotes and return as string literal
            return f'"{value}"'
        elif isinstance(value, bool):
            return "true" if value else "false"  
        elif value is None:
            return "null"
        else:
            return str(value)

    def visit_Name(self, node):
        """Handle name references."""
        return self.type_mapping.get(node.id, node.id)

    def visit_BinOp(self, node):
        """Handle binary operations."""
        left = self.visit_expr(node.left)
        right = self.visit_expr(node.right)
        op = self.get_operator(node.op)
        return f"({left} {op} {right})"

    def visit_Compare(self, node):
        """Handle comparison operations."""
        left = self.visit_expr(node.left)
        comparisons = []
        
        for i, (op, comparator) in enumerate(zip(node.ops, node.comparators)):
            right = self.visit_expr(comparator)
            op_str = self.get_comparison_operator(op)
            
            if i == 0:
                comparisons.append(f"{left} {op_str} {right}")
            else:
                comparisons.append(f"{op_str} {right}")
        
        return f"({' && '.join(comparisons)})"

    def visit_BoolOp(self, node):
        """Handle boolean operations."""
        op = "&&" if isinstance(node.op, ast.And) else "||"
        values = [self.visit_expr(value) for value in node.values]
        return f"({f' {op} '.join(values)})"

    def visit_Call(self, node):
        """Handle function calls."""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            
            # Handle built-in functions
            if func_name in self.function_mapping:
                cs_func = self.function_mapping[func_name]
                args = [self.visit_expr(arg) for arg in node.args]
                
                # Special cases for different function types
                if func_name == "print":
                    return f"Console.WriteLine({', '.join(args)})"
                elif func_name in ["len", "sum", "max", "min", "any", "all"]:
                    # These are methods on collections
                    if args:
                        return f"{args[0]}.{cs_func}({', '.join(args[1:])})"
                    return f"{cs_func}()"
                elif func_name == "range":
                    if len(args) == 1:
                        return f"Enumerable.Range(0, {args[0]})"
                    elif len(args) == 2:
                        return f"Enumerable.Range({args[0]}, {args[1]} - {args[0]})"
                    else:
                        return f"Enumerable.Range({args[0]}, {args[1]} - {args[0]}).Where((x, i) => i % {args[2]} == 0)"
                else:
                    return f"{cs_func}({', '.join(args)})"
            else:
                # Regular function call
                args = [self.visit_expr(arg) for arg in node.args]
                return f"{func_name}({', '.join(args)})"
        
        elif isinstance(node.func, ast.Attribute):
            # Method call
            obj = self.visit_expr(node.func.value)
            method = node.func.attr
            args = [self.visit_expr(arg) for arg in node.args]
            
            # Map Python methods to C# methods
            if method in self.method_mapping:
                method = self.method_mapping[method]
            
            return f"{obj}.{method}({', '.join(args)})"
        
        else:
            # Complex function call
            func = self.visit_expr(node.func)
            args = [self.visit_expr(arg) for arg in node.args]
            return f"{func}({', '.join(args)})"

    def visit_Attribute(self, node):
        """Handle attribute access."""
        obj = self.visit_expr(node.value)
        return f"{obj}.{node.attr}"

    def visit_Subscript(self, node):
        """Handle subscript operations."""
        obj = self.visit_expr(node.value)
        
        if isinstance(node.slice, ast.Slice):
            # Handle slicing
            start = self.visit_expr(node.slice.lower) if node.slice.lower else "0"
            stop = self.visit_expr(node.slice.upper) if node.slice.upper else f"{obj}.Count"
            
            # Convert to C# substring or Take/Skip for collections
            return f"{obj}.Skip({start}).Take({stop} - {start})"
        else:
            # Handle indexing
            index = self.visit_expr(node.slice)
            return f"{obj}[{index}]"

    def visit_List(self, node):
        """Handle list literals."""
        elements = [self.visit_expr(elt) for elt in node.elts]
        return f"new List<object> {{{', '.join(elements)}}}"

    def visit_Dict(self, node):
        """Handle dictionary literals."""
        items = []
        for key, value in zip(node.keys, node.values):
            key_str = self.visit_expr(key)
            value_str = self.visit_expr(value)
            items.append(f"[{key_str}] = {value_str}")
        
        return f"new Dictionary<object, object> {{{', '.join(items)}}}"

    def visit_Set(self, node):
        """Handle set literals."""
        elements = [self.visit_expr(elt) for elt in node.elts]
        return f"new HashSet<object> {{{', '.join(elements)}}}"

    def visit_JoinedStr(self, node):
        """Handle f-string literals."""
        # Convert f"Hello {name}" to $"Hello {name}"
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant):
                parts.append(value.value)
            elif isinstance(value, ast.FormattedValue):
                expr = self.visit_expr(value.value)
                parts.append(f"{{{expr}}}")
        
        return f'$"{"".join(parts)}"'

    def visit_FormattedValue(self, node):
        """Handle formatted values in f-strings."""
        expr = self.visit_expr(node.value)
        return f"{{{expr}}}"

    def get_operator(self, op):
        """Convert Python operators to C# operators."""
        operators = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
            ast.FloorDiv: '/',  # Integer division in C#
            ast.Mod: '%',
            ast.Pow: 'Math.Pow',  # Special case
            ast.LShift: '<<',
            ast.RShift: '>>',
            ast.BitOr: '|',
            ast.BitXor: '^',
            ast.BitAnd: '&',
        }
        return operators.get(type(op), '?')

    def get_unary_operator(self, op):
        """Convert Python unary operators to C# operators."""
        operators = {
            ast.UAdd: '+',
            ast.USub: '-',
            ast.Not: '!',
            ast.Invert: '~',
        }
        return operators.get(type(op), '?')

    def get_comparison_operator(self, op):
        """Convert Python comparison operators to C# operators."""
        operators = {
            ast.Eq: '==',
            ast.NotEq: '!=',
            ast.Lt: '<',
            ast.LtE: '<=',
            ast.Gt: '>',
            ast.GtE: '>=',
            ast.Is: '==',  # Reference equality
            ast.IsNot: '!=',
            ast.In: '.Contains',  # Special case
            ast.NotIn: '!.Contains',  # Special case
        }
        return operators.get(type(op), '?')

    def infer_type(self, node):
        """Infer C# type from Python expression."""
        if isinstance(node, ast.Constant):
            value = node.value
            if isinstance(value, int):
                return "int"
            elif isinstance(value, float):
                return "double"
            elif isinstance(value, str):
                return "string"
            elif isinstance(value, bool):
                return "bool"
            elif value is None:
                return "object"
        elif isinstance(node, ast.List):
            return "List<object>"
        elif isinstance(node, ast.Dict):
            return "Dictionary<object, object>"
        elif isinstance(node, ast.Set):
            return "HashSet<object>"
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in ["int", "float", "str", "bool"]:
                    return self.type_mapping[node.func.id]
        
        return "var"  # Use var for type inference


def translate_file(input_file, output_file=None):
    """Translate a Python file to C#."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            python_code = f.read()
        
        # Parse Python code into AST
        tree = ast.parse(python_code)
        
        # Translate to C#
        translator = PythonToCSharpTranslator()
        translator.visit(tree)
        
        # Generate output
        csharp_code = '\n'.join(translator.output)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(csharp_code)
            print(f"✅ Translation complete: {input_file} -> {output_file}")
        else:
            print(csharp_code)
        
        return csharp_code
        
    except FileNotFoundError:
        print(f"❌ Error: Input file '{input_file}' not found.")
        return None
    except SyntaxError as e:
        print(f"❌ Python syntax error: {e}")
        return None
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return None


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="🔄 Python to C# Code Translator",
        epilog="Example: python py_to_cs_agent.py input.py output.cs"
    )
    parser.add_argument('input_file', help='Input Python file (.py)')
    parser.add_argument('output_file', nargs='?', help='Output C# file (.cs) - optional')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"🔄 Translating: {args.input_file}")
        if args.output_file:
            print(f"📁 Output: {args.output_file}")
        else:
            print("📁 Output: stdout")
    
    # Perform translation
    result = translate_file(args.input_file, args.output_file)
    
    if result is None:
        sys.exit(1)
    
    if args.verbose:
        print("✅ Translation completed successfully!")


if __name__ == "__main__":
    main()
