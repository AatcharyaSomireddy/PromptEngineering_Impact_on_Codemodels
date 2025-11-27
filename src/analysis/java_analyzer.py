import subprocess, tempfile, os
from dataclasses import dataclass
from typing import List

import javalang

@dataclass
class CodeMetrics:
    lines_of_code: int
    cyclomatic_complexity: int
    compilation_success: bool
    syntax_errors: List[str]
    test_pass_rate: float

class JavaAnalyzer:
    def __init__(self, javac: str = "javac"):
        self.javac = javac

    def analyze_code(self, code: str, tests: List = None) -> CodeMetrics:
        syntax_err = self._check_syntax(code)
        comp_ok, comp_err = self._compile(code)
        loc = len([l for l in code.splitlines() if l.strip() and not l.strip().startswith("//")])
        cplx = self._complexity(code)
        return CodeMetrics(
            lines_of_code=loc,
            cyclomatic_complexity=cplx,
            compilation_success=comp_ok,
            syntax_errors=syntax_err + comp_err,
            test_pass_rate=0.0 if tests is None else self._run_tests(code, tests),
        )

    def _check_syntax(self, code):
        try:
            javalang.parse.parse(code)
            return []
        except Exception as e:
            return [str(e)]

    def _compile(self, code):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "Tmp.java")
            open(src, "w").write(code)
            res = subprocess.run([self.javac, src], capture_output=True, text=True)
            if res.returncode == 0:
                return True, []
            return False, res.stderr.splitlines()

    def _complexity(self, code):
        try:
            tree = javalang.parse.parse(code)
            return sum(
                1
                for _, node in tree
                if isinstance(
                    node,
                    (
                        javalang.tree.IfStatement,
                        javalang.tree.ForStatement,
                        javalang.tree.WhileStatement,
                        javalang.tree.SwitchStatement,
                        javalang.tree.ConditionalExpression,
                    ),
                )
            ) + 1
        except Exception:
            return 0

    def _run_tests(self, code, tests):
        return 0.0  # stub
