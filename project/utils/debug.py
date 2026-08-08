"""Utils for debugging.

Uses django's termcolors.

Available colors:

    color_names = ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')
"""

import sys
import os
import pytz

from datetime import tzinfo
from types import CodeType
from typing import Any, Optional

from django.conf import settings
from django.utils.termcolors import colorize
from django.utils import timezone


from pprint import pprint


class TerminalLoggingMixin:
    """Mixin for terminal logging."""

    def make_bold(self, text: str, fg="red") -> str:
        """Return text as bolded."""
        return colorize(text, opts=("bold",), fg=fg)

    def pprint_symbols(self, symbol="=", symbol_repetition=42, color="green") -> None:
        """Print colorized symbol repeated."""
        print(
            colorize(symbol * symbol_repetition, opts=("bold",), fg=color, bg="black")
        )

    def pprint_label(
        self, label="Data", symbol="=", symbol_repetition=20, fg="green", bg="black"
    ) -> None:
        """Prints label string, surrounded by repeated symbols, colorized."""
        symboled_label = "{} {} {}".format(
            symbol * symbol_repetition, label, symbol * symbol_repetition
        )
        print(colorize(symboled_label, opts=("bold",), fg=fg, bg=bg))

    def pprint_data(self, data: Any, label="Data", fg="green", bg="black") -> None:
        """Pretty print data with label."""
        print()
        self.pprint_label(label=label, fg=fg, bg=bg)
        pprint(data)
        print()

    def pprint_response(
        self, response: Any, label="Response", fg="blue", bg="black"
    ) -> None:
        """Pretty print response, a shorthand for pprint_data(data=response, label='Response')"""
        self.pprint_data(data=response, label=label, fg=fg, bg=bg)

    def pprint_exception(
        self, exception: Exception, label="Exception", fg="red", bg="black"
    ) -> None:
        """Pretty print exception string, a shorthand for pprint_data(data=str(exception), label='Exception')"""
        self.pprint_data(data=str(exception), label=label, fg=fg, bg=bg)

    def pprint_type(self, data: Any, label="Type", fg="magenta", bg="black") -> None:
        """Pretty print type of object data."""
        self.pprint_data(type(data), label=label, fg=fg, bg=bg)

    def pprint_dir(self, data: Any, label="dir(data)", fg="cyan", bg="black") -> None:
        """Pretty print dir(data)."""
        try:
            self.pprint_data(dir(data), label=label, fg=fg, bg=bg)
        except Exception:
            self.pprint_label("{} has no .__dir__ attribute".format(data))

    def pprint_dict(
        self, data: Any, label="data.__dict__", fg="cyan", bg="black"
    ) -> None:
        """Pretty print data.__dict__."""
        try:
            self.pprint_data(data.__dict__, label=label, fg=fg, bg=bg)
        except Exception:
            self.pprint_label(label="{} has no .__dict__ attribute".format(data), bg=bg)

    def pprint_breakpoint(self, label="BREAK POINT", symbol="*") -> None:
        """Print a break point line."""
        print()
        self.pprint_label(label, symbol=symbol, symbol_repetition=30, bg="red")
        print()

    def pprint_locals(
        self, local_vars: dict, label: Optional[str] = "Local Variables"
    ) -> None:
        """Pretty print local variables `local_vars` from locals() returned dictionary.

        Sample invocation:
            self.pprint_locals(locals())
        """
        self.pprint_data(data=local_vars, label=label)

    def debugger(self, message="Paused in debugger") -> None:
        """Stop execution, mimiced from javascript `debugger` statement."""
        raise RuntimeError(message)

    def pprint_and_debug(self, data: Any, label="Data", fg="green", bg="black") -> None:
        """Pretty print data and raise RuntimeError for debuggin."""
        self.pprint_data(data=data, label=label, fg=fg, bg=bg)
        self.debugger()


class DebuggerMixin(TerminalLoggingMixin):
    """Debugger mixin."""

    def print_debug_multiline(
        self,
        label: str,
        timestamp: str,
        exception_object: Exception,
        exception_type: type,
        caller: str,
        location: str,
        line_number: int,
        color: str,
    ) -> None:
        """Print exception info nicely in multilines with label."""
        try:
            print()
            self.pprint_label(label, fg=color, bg="black")
            print("Timestamp:", self.make_bold(timestamp, fg=color))
            print("Exception:", self.make_bold(str(exception_object), fg=color))
            print("Type:", self.make_bold(exception_type.__name__, fg=color))
            print("Caller:", self.make_bold(text="{}()".format(caller), fg=color))
            print("Location:", self.make_bold(location, fg=color))
            print("Line:", self.make_bold(line_number, fg=color))
            self.pprint_symbols(symbol_repetition=42 + len(label), color="red")
        except Exception as exc:
            self.pprint_exception(exc, "Exception occured on trying to debug exception")
            self.pprint_exception(exception_object)

    def print_debug_single_line(
        self,
        timestamp: str,
        exception_object: Exception,
        exception_type: type,
        location: str,
        caller: str,
        line_number: int,
        color: str,
    ) -> None:
        """Print exception info in single line."""
        try:
            one_line_error = "{} -> Exception:{} -> Type:{} -> Caller:{}() -> Location:{} -> Line:{}".format(
                timestamp,
                exception_object,
                exception_type.__name__,
                caller,
                location,
                line_number,
            )
            print(colorize(one_line_error, opts=("bold", "underscore"), fg=color))
        except Exception as exc:
            self.pprint_exception(exc, "Exception occured on trying to debug exception")
            self.pprint_exception(exception_object)

    def get_caller(self, code_type: CodeType) -> str:
        """Get caller string."""
        code = code_type.co_name
        caller = code
        instance_name = self.__class__.__name__
        if instance_name != "DebuggerMixin":
            caller = "{}.{}".format(instance_name, code)

        return caller

    def get_project_root_dir(self) -> str:
        """Return project root directory string."""
        return str(settings.BASE_DIR.parent)

    def get_location(self, code_type: CodeType) -> str:
        """Return file location."""
        root = self.get_project_root_dir()
        fullpath = code_type.co_filename
        location = fullpath.split(root)[1]

        return location

    def is_debug_multiline(self) -> bool:
        """Check if to print debug line in multiline."""
        try:
            return os.environ.get("DEBUG_MULTILINE") == "True"
        except Exception:
            return False

    def is_debug_timezone_ph(self) -> bool:
        """Check if print debug in PH time."""
        try:
            return os.environ.get("DEBUG_TIMEZONE_PH") == "True"
        except Exception as exc:
            return False

    def get_debug_timezone(self) -> tzinfo:
        """Get debug timezone."""
        au_melbourne = pytz.timezone("Australia/Melbourne")
        asia_singapore = pytz.timezone("Asia/Singapore")

        debug_timezone = au_melbourne
        if self.is_debug_timezone_ph():
            debug_timezone = asia_singapore

        return debug_timezone

    def get_timestamp(self) -> str:
        """Return current timestamp on this format:

        2022-05-06 02:35 AM
        """
        date_format = "%Y-%m-%d"
        time_format = "%I:%M %p "
        datetime_format = date_format + " " + time_format

        timezone_now = timezone.now()
        debug_timezone = self.get_debug_timezone()
        timestamp = timezone_now.astimezone(debug_timezone)
        timestamp_string = timestamp.strftime(datetime_format)

        return timestamp_string

    def debug_exception(
        self, exception: Exception, label="Exception Occurred", color="red"
    ) -> None:
        """Print exception and traceback info for developers to debug.

        NOTE: This should be called on the context of an except clause:
        ..
        except Exception as exc:
            self.debug_exception(exc)
        ..

        https://docs.python.org/3/library/sys.html#sys.exc_info
        """
        try:
            exception_type, exception_object, exception_traceback = sys.exc_info()

            exception_frame = exception_traceback.tb_frame
            code_type = exception_frame.f_code

            caller = self.get_caller(code_type)
            location = self.get_location(code_type)
            line_number = exception_traceback.tb_lineno
            timestamp = self.get_timestamp()

            if self.is_debug_multiline():
                self.print_debug_multiline(
                    label,
                    timestamp,
                    exception_object,
                    exception_type,
                    caller,
                    location,
                    line_number,
                    color,
                )
            else:
                self.print_debug_single_line(
                    timestamp,
                    exception_object,
                    exception_type,
                    location,
                    caller,
                    line_number,
                    color,
                )

        except Exception as e:
            self.pprint_exception(e, "Exception occured on trying to debug exception")
            self.pprint_exception(exception, "Exception")
