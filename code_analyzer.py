#!/usr/bin/env python3
"""
Code Analyzer for providing context-aware hints
Analyzes user's code to understand their current approach and provide targeted hints
"""

import re
import ast
from typing import Dict, List, Optional, Set


class CodeAnalyzer:
    """Analyzes Python code to extract information for context-aware hints."""
    
    def __init__(self):
        self.common_patterns = {
            'two_pointers': ['left', 'right', 'l', 'r', 'start', 'end'],
            'sliding_window': ['window', 'start', 'end', 'left', 'right'],
            'hash_map': ['dict', 'hashmap', 'map', 'dictionary'],
            'hash_set': ['set', 'hashset'],
            'stack': ['stack', 'append', 'pop'],
            'queue': ['queue', 'deque', 'popleft'],
            'binary_search': ['mid', 'middle', 'low', 'high', 'left', 'right'],
            'dp': ['dp', 'memo', 'memoization', 'cache'],
            'bfs': ['queue', 'deque', 'bfs', 'level'],
            'dfs': ['dfs', 'recursive', 'recurse'],
            'backtracking': ['backtrack', 'path', 'result'],
            'sort': ['sort', 'sorted'],
            'heap': ['heap', 'heapq', 'priority']
        }
    
    def analyze_code(self, code: str, question_category: str = '') -> Dict:
        """
        Analyze user's code to understand their approach.
        
        Args:
            code: User's Python code
            question_category: Category of the question (e.g., "Two Pointers", "Hash Table")
            
        Returns:
            Dictionary with analysis results
        """
        analysis = {
            'has_solution_class': False,
            'has_method': False,
            'method_name': None,
            'variables_used': [],
            'data_structures': [],
            'patterns_detected': [],
            'control_structures': [],
            'lines_of_code': 0,
            'has_return': False,
            'has_loop': False,
            'has_conditionals': False,
            'code_complexity': 'unknown',
            'suggestions': []
        }
        
        if not code or not code.strip():
            return analysis
        
        # Count lines (non-empty)
        lines = [line.strip() for line in code.split('\n') if line.strip() and not line.strip().startswith('#')]
        analysis['lines_of_code'] = len(lines)
        
        # Extract variables and data structures
        analysis['variables_used'] = self._extract_variables(code)
        analysis['data_structures'] = self._detect_data_structures(code)
        analysis['patterns_detected'] = self._detect_patterns(code, analysis['variables_used'])
        analysis['control_structures'] = self._detect_control_structures(code)
        
        # Check for Solution class
        analysis['has_solution_class'] = 'class Solution' in code
        
        # Extract method name
        method_match = re.search(r'def\s+(\w+)\s*\(', code)
        if method_match:
            analysis['has_method'] = True
            analysis['method_name'] = method_match.group(1)
        
        # Check for return statement
        analysis['has_return'] = 'return' in code
        
        # Check for loops
        analysis['has_loop'] = bool(re.search(r'\b(for|while)\s+', code))
        
        # Check for conditionals
        analysis['has_conditionals'] = bool(re.search(r'\b(if|elif|else)\s+', code))
        
        # Try to parse AST for deeper analysis
        try:
            tree = ast.parse(code)
            ast_analysis = self._analyze_ast(tree)
            analysis.update(ast_analysis)
        except SyntaxError:
            # Code has syntax errors, but we can still provide basic analysis
            pass
        
        # Generate suggestions based on analysis
        analysis['suggestions'] = self._generate_suggestions(analysis, question_category)
        
        return analysis
    
    def _extract_variables(self, code: str) -> List[str]:
        """Extract variable names from code."""
        variables = set()
        
        # Simple regex to find variable assignments
        # Match: variable_name = ...
        var_pattern = r'\b([a-z_][a-z0-9_]*)\s*='
        matches = re.findall(var_pattern, code)
        variables.update(matches)
        
        # Also find variables in function parameters
        param_pattern = r'def\s+\w+\s*\([^)]*([a-z_][a-z0-9_]*(?:\s*,\s*[a-z_][a-z0-9_]*)*)'
        param_matches = re.findall(param_pattern, code)
        for params in param_matches:
            variables.update([p.strip() for p in params.split(',')])
        
        return sorted(list(variables))
    
    def _detect_data_structures(self, code: str) -> List[str]:
        """Detect which data structures are being used."""
        structures = []
        code_lower = code.lower()
        
        if 'dict' in code_lower or '{}' in code or 'dictionary' in code_lower:
            structures.append('dict')
        if 'set' in code_lower or 'set(' in code:
            structures.append('set')
        if 'list' in code_lower or '[]' in code or 'array' in code_lower:
            structures.append('list')
        if 'stack' in code_lower:
            structures.append('stack')
        if 'queue' in code_lower or 'deque' in code_lower:
            structures.append('queue')
        if 'heap' in code_lower or 'heapq' in code_lower:
            structures.append('heap')
        
        return structures
    
    def _detect_patterns(self, code: str, variables: List[str]) -> List[str]:
        """Detect algorithmic patterns based on code structure."""
        patterns = []
        code_lower = code.lower()
        var_lower = ' '.join([v.lower() for v in variables])
        combined = code_lower + ' ' + var_lower
        
        # Check for two pointers pattern
        if any(term in combined for term in self.common_patterns['two_pointers']):
            if 'left' in combined and 'right' in combined:
                patterns.append('two_pointers')
        
        # Check for sliding window
        if any(term in combined for term in self.common_patterns['sliding_window']):
            if 'window' in combined or ('start' in combined and 'end' in combined):
                patterns.append('sliding_window')
        
        # Check for hash map
        if any(term in combined for term in self.common_patterns['hash_map']):
            if 'dict' in code_lower or '{}' in code:
                patterns.append('hash_map')
        
        # Check for hash set
        if any(term in combined for term in self.common_patterns['hash_set']):
            if 'set' in code_lower:
                patterns.append('hash_set')
        
        # Check for stack
        if any(term in combined for term in self.common_patterns['stack']):
            if 'append' in code_lower and 'pop' in code_lower:
                patterns.append('stack')
        
        # Check for binary search
        if any(term in combined for term in self.common_patterns['binary_search']):
            if 'mid' in combined or 'middle' in combined:
                patterns.append('binary_search')
        
        # Check for DP
        if any(term in combined for term in self.common_patterns['dp']):
            patterns.append('dp')
        
        # Check for BFS/DFS
        if any(term in combined for term in self.common_patterns['bfs']):
            patterns.append('bfs')
        if any(term in combined for term in self.common_patterns['dfs']):
            patterns.append('dfs')
        
        # Check for backtracking
        if any(term in combined for term in self.common_patterns['backtracking']):
            patterns.append('backtracking')
        
        return patterns
    
    def _detect_control_structures(self, code: str) -> List[str]:
        """Detect control structures used in code."""
        structures = []
        
        if re.search(r'\bfor\s+', code):
            structures.append('for_loop')
        if re.search(r'\bwhile\s+', code):
            structures.append('while_loop')
        if re.search(r'\bif\s+', code):
            structures.append('if_statement')
        if re.search(r'\bdef\s+', code):
            structures.append('function')
        if re.search(r'\bclass\s+', code):
            structures.append('class')
        
        return structures
    
    def _analyze_ast(self, tree: ast.AST) -> Dict:
        """Perform AST-based analysis."""
        analysis = {
            'function_calls': [],
            'imports': [],
            'complexity_score': 0
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    analysis['function_calls'].append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    analysis['function_calls'].append(node.func.attr)
            
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    analysis['imports'].append(alias.name)
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    analysis['imports'].append(node.module)
        
        # Calculate simple complexity score
        analysis['complexity_score'] = len(analysis['function_calls']) + len(analysis['imports'])
        
        return analysis
    
    def _generate_suggestions(self, analysis: Dict, question_category: str) -> List[str]:
        """Generate suggestions based on code analysis."""
        suggestions = []
        
        # Check if code is empty or just template
        if analysis['lines_of_code'] <= 2 or not analysis['has_method']:
            suggestions.append("Start by thinking about the data structure you need.")
            if question_category:
                suggestions.append(f"For {question_category} problems, consider the common patterns for this category.")
            return suggestions
        
        # Check if return statement is missing
        if not analysis['has_return'] and analysis['lines_of_code'] > 3:
            suggestions.append("Don't forget to return your result!")
        
        # Category-specific suggestions
        category_lower = question_category.lower()
        
        if 'two pointer' in category_lower or 'sliding window' in category_lower:
            if 'two_pointers' not in analysis['patterns_detected']:
                suggestions.append("Consider using two pointers: one starting from the left, one from the right.")
            if not analysis['has_loop']:
                suggestions.append("You'll likely need a loop to move your pointers.")
        
        if 'hash' in category_lower or 'set' in category_lower:
            if 'hash_map' not in analysis['patterns_detected'] and 'hash_set' not in analysis['patterns_detected']:
                suggestions.append("Consider using a hash map or set to track elements you've seen.")
        
        if 'stack' in category_lower:
            if 'stack' not in analysis['data_structures']:
                suggestions.append("This problem might benefit from using a stack data structure.")
        
        if 'binary search' in category_lower:
            if 'binary_search' not in analysis['patterns_detected']:
                suggestions.append("For binary search, you'll need left, right, and mid pointers.")
        
        # General suggestions
        if not analysis['has_loop'] and analysis['lines_of_code'] > 5:
            suggestions.append("You might need a loop to iterate through the input.")
        
        if not analysis['has_conditionals'] and analysis['lines_of_code'] > 5:
            suggestions.append("Consider adding conditional logic to handle different cases.")
        
        return suggestions
    
    def get_code_summary(self, analysis: Dict) -> str:
        """Generate a summary of the code analysis for LLM prompt."""
        summary_parts = []
        
        if analysis['has_solution_class']:
            summary_parts.append("The code has a Solution class.")
        else:
            summary_parts.append("The code does not have a Solution class.")
        
        if analysis['has_method']:
            summary_parts.append(f"Method name: {analysis['method_name']}")
        else:
            summary_parts.append("No method definition found.")
        
        if analysis['variables_used']:
            summary_parts.append(f"Variables used: {', '.join(analysis['variables_used'][:10])}")
        
        if analysis['data_structures']:
            summary_parts.append(f"Data structures: {', '.join(analysis['data_structures'])}")
        
        if analysis['patterns_detected']:
            summary_parts.append(f"Patterns detected: {', '.join(analysis['patterns_detected'])}")
        
        if analysis['has_loop']:
            summary_parts.append("Uses loops.")
        
        if analysis['has_conditionals']:
            summary_parts.append("Uses conditional statements.")
        
        if analysis['has_return']:
            summary_parts.append("Has return statement.")
        else:
            summary_parts.append("Missing return statement.")
        
        if analysis['suggestions']:
            summary_parts.append(f"Suggestions: {'; '.join(analysis['suggestions'])}")
        
        return ". ".join(summary_parts)

