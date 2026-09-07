import os

import pytest

from src.decorators import log


class TestLogToConsole:
    """Тесты логирования в консоль (filename не задан)."""

    def test_success_console(self, capsys):
        @log()
        def add(a, b):
            return a + b

        result = add(1, 2)
        captured = capsys.readouterr()
        assert result == 3
        assert "add ok" in captured.out

    def test_error_console(self, capsys):
        @log()
        def divide(a, b):
            return a / b

        with pytest.raises(ZeroDivisionError):
            divide(1, 0)
        captured = capsys.readouterr()
        assert "divide error" in captured.out
        assert "Inputs: (1, 0), {}" in captured.out

    def test_kwargs_in_error_console(self, capsys):
        @log()
        def greet(name, greeting="Hi"):
            raise ValueError("oops")

        with pytest.raises(ValueError):
            greet("Bob", greeting="Hello")
        captured = capsys.readouterr()
        assert "greet error" in captured.out
        assert "Inputs:" in captured.out

    def test_no_args_success_console(self, capsys):
        @log()
        def ping():
            return "pong"

        result = ping()
        captured = capsys.readouterr()
        assert result == "pong"
        assert "ping ok" in captured.out


class TestLogToFile:
    """Тесты логирования в файл."""

    def test_success_file(self, tmp_path):
        log_file = tmp_path / "test_log.txt"

        @log(filename=str(log_file))
        def add(a, b):
            return a + b

        add(1, 2)
        content = log_file.read_text(encoding="utf-8")
        assert "add ok" in content

    def test_error_file(self, tmp_path):
        log_file = tmp_path / "test_log.txt"

        @log(filename=str(log_file))
        def divide(a, b):
            return a / b

        with pytest.raises(ZeroDivisionError):
            divide(10, 0)
        content = log_file.read_text(encoding="utf-8")
        assert "divide error" in content
        assert "Inputs: (10, 0), {}" in content

    def test_multiple_calls_append_file(self, tmp_path):
        log_file = tmp_path / "test_log.txt"

        @log(filename=str(log_file))
        def square(x):
            return x * x

        square(3)
        square(4)
        content = log_file.read_text(encoding="utf-8")
        assert content.count("square ok") == 2

    def test_file_not_raises_on_success(self, tmp_path):
        log_file = tmp_path / "nested" / "dir" / "log.txt"

        @log(filename=str(log_file))
        def echo(x):
            return x

        echo("hello")
        assert log_file.exists()
        assert "echo ok" in log_file.read_text(encoding="utf-8")


class TestLogEdgeCases:
    """Краевые случаи."""

    def test_preserves_function_name(self):
        @log()
        def my_func():
            """Docstring."""
            return 42

        assert my_func.__name__ == "my_func"
        assert my_func.__doc__ == "Docstring."

    def test_re_raises_exception(self, capsys):
        @log()
        def fail():
            raise RuntimeError("boom")

        with pytest.raises(RuntimeError, match="boom"):
            fail()
        captured = capsys.readouterr()
        assert "fail error" in captured.out

    def test_returns_correct_result(self, capsys):
        @log()
        def multiply(a, b):
            return a * b

        assert multiply(3, 4) == 12
        capsys.readouterr()  # очищаем вывод

    def test_no_filename_prints_to_stdout(self, capsys):
        @log()
        def hello():
            return "world"

        hello()
        captured = capsys.readouterr()
        assert "hello ok\n" == captured.out
