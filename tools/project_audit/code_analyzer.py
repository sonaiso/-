"""
Static Code Analyzer for Dashboard Metrics
محلل الكود الثابت لمقاييس لوحة القياس

Analyzes source code to extract:
- Typed contracts (@dataclass, Protocol, Enum)
- Evidence usage
- Rank policies
- Residual taxonomy
- Trace/replay patterns
"""

import ast
import os
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class CodeMetrics:
    """Metrics extracted from code analysis"""
    # Files
    source_files: List[str] = field(default_factory=list)
    test_files: List[str] = field(default_factory=list)
    doc_files: List[str] = field(default_factory=list)

    # Type annotations
    dataclass_count: int = 0
    frozen_dataclass_count: int = 0
    protocol_count: int = 0
    enum_count: int = 0
    typed_function_count: int = 0
    total_function_count: int = 0

    # Patterns
    result_instantiations: int = 0
    result_with_trace: int = 0
    evidence_usages: int = 0
    rank_checks: int = 0
    residual_classifications: int = 0

    # Lines of code
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0


@dataclass
class LayerCodeInfo:
    """Code information for a specific layer"""
    layer_id: str
    contract_files: List[str] = field(default_factory=list)
    implementation_files: List[str] = field(default_factory=list)
    test_files: List[str] = field(default_factory=list)
    doc_files: List[str] = field(default_factory=list)

    has_typed_contract: bool = False
    uses_strings_not_types: bool = False
    has_tests: bool = False
    has_noleap_tests: bool = False
    has_golden_dataset: bool = False

    evidence_count: int = 0
    residual_count: int = 0
    trace_count: int = 0


class StaticCodeAnalyzer:
    """Analyzes Python source code for governance metrics"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.src_root = project_root / "src"
        self.tests_root = project_root / "tests"
        self.docs_root = project_root / "docs"

    def analyze_file(self, file_path: Path) -> CodeMetrics:
        """Analyze a single Python file"""
        metrics = CodeMetrics()

        if not file_path.exists() or not file_path.suffix == '.py':
            return metrics

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content, filename=str(file_path))

            # Count lines
            lines = content.split('\n')
            metrics.total_lines = len(lines)
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    metrics.blank_lines += 1
                elif stripped.startswith('#'):
                    metrics.comment_lines += 1
                else:
                    metrics.code_lines += 1

            # Analyze AST
            for node in ast.walk(tree):
                # Count dataclasses
                if isinstance(node, ast.ClassDef):
                    for decorator in node.decorator_list:
                        if self._is_dataclass_decorator(decorator):
                            metrics.dataclass_count += 1
                            if self._is_frozen_dataclass(decorator):
                                metrics.frozen_dataclass_count += 1

                    # Check for Protocol
                    for base in node.bases:
                        if isinstance(base, ast.Name) and base.id == 'Protocol':
                            metrics.protocol_count += 1

                    # Check for Enum
                    for base in node.bases:
                        if isinstance(base, ast.Name) and base.id == 'Enum':
                            metrics.enum_count += 1

                # Count functions with type hints
                if isinstance(node, ast.FunctionDef):
                    metrics.total_function_count += 1
                    if node.returns or any(arg.annotation for arg in node.args.args):
                        metrics.typed_function_count += 1

                # Count Result instantiations
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == 'Result':
                        metrics.result_instantiations += 1
                        # Check for trace argument
                        for keyword in node.keywords:
                            if keyword.arg == 'trace':
                                metrics.result_with_trace += 1

            # Pattern matching in source
            metrics.evidence_usages = len(re.findall(r'Evidence\(', content))
            metrics.rank_checks = len(re.findall(r'Rank\.|rank\s*[=!<>]', content))
            metrics.residual_classifications = len(re.findall(r'residuals\s*=|Residual\(', content))

        except Exception as e:
            # Silently skip files with parse errors
            pass

        return metrics

    def _is_dataclass_decorator(self, decorator: ast.expr) -> bool:
        """Check if decorator is @dataclass"""
        if isinstance(decorator, ast.Name) and decorator.id == 'dataclass':
            return True
        if isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name) and decorator.func.id == 'dataclass':
                return True
        return False

    def _is_frozen_dataclass(self, decorator: ast.expr) -> bool:
        """Check if dataclass has frozen=True"""
        if isinstance(decorator, ast.Call):
            for keyword in decorator.keywords:
                if keyword.arg == 'frozen':
                    if isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        return True
        return False

    def analyze_directory(self, directory: Path, pattern: str = "**/*.py") -> CodeMetrics:
        """Analyze all Python files in a directory"""
        combined = CodeMetrics()

        for file_path in directory.glob(pattern):
            if file_path.is_file():
                metrics = self.analyze_file(file_path)
                combined = self._merge_metrics(combined, metrics)

        return combined

    def _merge_metrics(self, a: CodeMetrics, b: CodeMetrics) -> CodeMetrics:
        """Merge two CodeMetrics objects"""
        return CodeMetrics(
            source_files=a.source_files + b.source_files,
            test_files=a.test_files + b.test_files,
            doc_files=a.doc_files + b.doc_files,
            dataclass_count=a.dataclass_count + b.dataclass_count,
            frozen_dataclass_count=a.frozen_dataclass_count + b.frozen_dataclass_count,
            protocol_count=a.protocol_count + b.protocol_count,
            enum_count=a.enum_count + b.enum_count,
            typed_function_count=a.typed_function_count + b.typed_function_count,
            total_function_count=a.total_function_count + b.total_function_count,
            result_instantiations=a.result_instantiations + b.result_instantiations,
            result_with_trace=a.result_with_trace + b.result_with_trace,
            evidence_usages=a.evidence_usages + b.evidence_usages,
            rank_checks=a.rank_checks + b.rank_checks,
            residual_classifications=a.residual_classifications + b.residual_classifications,
            total_lines=a.total_lines + b.total_lines,
            code_lines=a.code_lines + b.code_lines,
            comment_lines=a.comment_lines + b.comment_lines,
            blank_lines=a.blank_lines + b.blank_lines,
        )

    def analyze_layer(self, layer_id: str, layer_paths: Dict[str, List[str]]) -> LayerCodeInfo:
        """
        Analyze code for a specific layer

        Args:
            layer_id: Layer identifier (e.g., "A2")
            layer_paths: Dict with keys 'contracts', 'implementations', 'tests', 'docs'
        """
        info = LayerCodeInfo(layer_id=layer_id)

        # Collect files
        info.contract_files = layer_paths.get('contracts', [])
        info.implementation_files = layer_paths.get('implementations', [])
        info.test_files = layer_paths.get('tests', [])
        info.doc_files = layer_paths.get('docs', [])

        # Analyze contract files
        has_dataclass = False
        has_frozen = False
        uses_strings = False

        for file_path_str in info.contract_files:
            file_path = self.project_root / file_path_str
            metrics = self.analyze_file(file_path)

            if metrics.dataclass_count > 0:
                has_dataclass = True
            if metrics.frozen_dataclass_count > 0:
                has_frozen = True

            # Check for string-based patterns (simplified heuristic)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Look for string literals used as type placeholders
                    if re.search(r':\s*str\s*=.*#.*(?:type|candidate|status)', content):
                        uses_strings = True
            except:
                pass

        info.has_typed_contract = has_dataclass and has_frozen
        info.uses_strings_not_types = uses_strings and not has_frozen

        # Check for tests
        info.has_tests = len(info.test_files) > 0

        # Check for NoLeap tests
        for test_file in info.test_files:
            test_path = self.project_root / test_file
            if test_path.exists():
                try:
                    with open(test_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'noleap' in content.lower() or 'test_noleap' in content.lower():
                            info.has_noleap_tests = True
                            break
                except:
                    pass

        # Check for golden dataset
        for test_file in info.test_files:
            test_path = self.project_root / test_file
            if test_path.exists():
                try:
                    with open(test_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'golden' in content.lower() or 'GOLDEN_' in content:
                            info.has_golden_dataset = True
                            break
                except:
                    pass

        # Count evidence, residuals, trace
        for impl_file in info.implementation_files:
            impl_path = self.project_root / impl_file
            if impl_path.exists():
                metrics = self.analyze_file(impl_path)
                info.evidence_count += metrics.evidence_usages
                info.residual_count += metrics.residual_classifications
                info.trace_count += metrics.result_with_trace

        return info

    def find_layer_files(self, layer_keywords: List[str]) -> Dict[str, List[str]]:
        """
        Find files related to a layer by keywords

        Args:
            layer_keywords: List of keywords to search for (e.g., ["dal", "pure_dal"])

        Returns:
            Dict with 'contracts', 'implementations', 'tests', 'docs' lists
        """
        result = {
            'contracts': [],
            'implementations': [],
            'tests': [],
            'docs': []
        }

        # Search in src/
        if self.src_root.exists():
            for pattern in layer_keywords:
                for file in self.src_root.glob(f"**/*{pattern}*.py"):
                    rel_path = str(file.relative_to(self.project_root))
                    if 'test' not in rel_path.lower():
                        if any(kw in file.name.lower() for kw in ['candidate', 'structure', 'contract']):
                            result['contracts'].append(rel_path)
                        else:
                            result['implementations'].append(rel_path)

        # Search in tests/
        if self.tests_root.exists():
            for pattern in layer_keywords:
                for file in self.tests_root.glob(f"**/*{pattern}*.py"):
                    rel_path = str(file.relative_to(self.project_root))
                    result['tests'].append(rel_path)

        # Search in docs/
        if self.docs_root.exists():
            for pattern in layer_keywords:
                for file in self.docs_root.glob(f"**/*{pattern}*.md"):
                    rel_path = str(file.relative_to(self.project_root))
                    result['docs'].append(rel_path)

        return result
