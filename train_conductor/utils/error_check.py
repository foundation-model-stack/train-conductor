# Copyright The Train Conductor Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Standard
from collections.abc import Iterable
from types import GeneratorType
from typing import Any
import os


def type_check(log_code, *types, allow_none=False, **variables):
    """Check for acceptable types for a given object.  If the type check fails, a log message
    will be emitted at the error level on the log channel associated with this handler and a
    `TypeError` exception will be raised with an appropriate message.  This check should be used
    to check for appropriate variable types.  For example, to verify that an argument passed to
    a function that expects a string is actually an instance of a string.

    Args:
        log_code (str): A log code with format `<COR90063501E>` where `COR`
            is a short code for the library (for `caikit_core` in this
            example) and where `90063501` is a unique eight-digit identifier
            (example generation in `scripts/cor_log_code`) and where `E` is
            an error level short-code, one of `{'fatal': 'F', 'error': 'E',
            'warning': 'W', 'info': 'I', 'trace': 'T', 'debug': 'D'}`.
        *types (type or None): Variadic arguments containing all acceptable
            types for `variables`.  If any values of `variable` are not any
            of `*types` then a log message will be emitted and a `TypeError`
            will be raised.  Multiple types may be specified as separate
            arguments. If no types are specified, then a `RuntimeError` will
            be raised.
        allow_none (bool): If `True` then the values of `variables` are
            allowed to take on the value of `None` without causing the type
            check to fail.  If `False` (default) then `None` values will
            cause the type check to fail.
        **variables (object): Variadic keyword arguments to be examined for
            acceptable type.  The name of the variable is used in log and
            error messages while its value is actually check against
            `types`.  Multiple keyword variables may be specified.  If no
            variables are specified, then a `RuntimeError` will be raised.

    Examples:
        # this will raise a `TypeError` because `foo` is not `None` or a `list` or `tuple`
        > error.type_check('<COR99962332E>', None, list, tuple, foo='hello world')

        # this type check verifies that `foo` and `bar` are both strings
        > error.type_check('<COR03761101E>', str, foo=foo, bar=bar)
    """

    if not types:
        raise RuntimeError(log_code, "invalid type check: no types specified")

    if not variables:
        raise RuntimeError(log_code, "invalid type check: no variables specified")

    for name, variable in variables.items():
        if allow_none and variable is None:
            continue

        # check if variable is an instance of one of `types`
        if not isinstance(variable, types):
            type_name = type(variable).__name__
            valid_type_names = tuple(typ.__name__ for typ in types)
            if allow_none:
                valid_type_names += (type(None).__name__,)

            # create, log and raise an appropriate exception
            raise TypeError(log_code,
                    "type check failed: variable `{}` has type `{}` "
                    "(fully qualified name `{}`) not in `{}`".format(
                        name, type_name, _fqname(variable), valid_type_names
                    )
                )


def type_check_all(log_code, *types, allow_none=False, **variables):
    """This type check is similar to `.type_check` except that it verifies that each variable
    in `**variables` is either a `list` or a `tuple` and then checks that *all* of the items
    they contain are instances of a type in `*types`.  If `allow_none` is set to `True`, then
    the variable is allowed to be `None`, but the items in the `list` or `tuple` are not.

    Examples:
        # this type check will verify that foo is a `list` or `tuple` containing only `int`s
        > foo = (1, 2, 3)
        > error.type_check('<COR50993928E>', int, foo='hello world')

        # this type check allows `foo` to be `None`
        > error.type_check('<COR79540602E>', None, foo=None)

        # this type check fails because `foo` contains `None`
        > error.type_check('<COR87797257E>', None, int, foo=(1, 2, None, 3, 4))

        # this type check fails because `bar` contains a `str`
        # but not for any other reason
        > foo = [1, 2, 3]
        > bar = [4, 5, 'x']
        > baz = None
        > error.type_check('<COR40818868E>', None, int, foo=foo, bar=bar, baz=None)
    """

    if not types:
        raise RuntimeError(log_code, "invalid type check: no types specified")

    if not variables:
        raise RuntimeError(log_code, "invalid type check: no variables specified")

    top_level_types = (Iterable,)
    invalid_types = (
        str,
        GeneratorType,
    )  # top level types that will fail the type check

    for name, variable in variables.items():
        if allow_none and variable is None:
            continue

        # log and raise if variable is not an Iterable
        if not isinstance(variable, top_level_types) or isinstance(
            variable, invalid_types
        ):
            type_name = type(variable).__name__
            valid_type_names = tuple(typ.__name__ for typ in top_level_types)
            if allow_none:
                valid_type_names += (type(None).__name__,)

            raise TypeError(log_code,
                    "type check failed: variable `{}` has type `{}` not in `{}`".format(
                        name, type_name, valid_type_names
                    )
                )

        # log and raise if any item is not in list of valid types
        for item in variable:
            if not isinstance(item, types):
                type_name = type(item).__name__
                valid_type_names = tuple(typ.__name__ for typ in types)

                raise TypeError(log_code,
                        "type check failed: element of `{}` has type `{}` not in `{}`".format(
                            name, type_name, valid_type_names
                        )
                    )

def subclass_check(
    log_code, child_class: Any, *parent_classes, allow_none: bool = False
):
    """Check that the given child classes are valid types and that they
    derive from the given set of parent classes [issubclass(x, (y, z))]. If
    the subclass check fails, a log message will be emitted at the error
    level on the log channel associated with this handler and a `TypeError`
    exception will be raised with an appropriate message. This check should
    be used to check that a given class meets the interface of a parent
    class. For example, to verify that a class handle is a valid ModuleBase
    subclass.

    Args:
        log_code (str): A log code with format `<COR90063501E>` where `COR`
            is a short code for the library (for `caikit_core` in this
            example) and where `90063501` is a unique eight-digit identifier
            and where `E` is an error level short-code, one of `{'fatal':
            'F', 'error': 'E', 'warning': 'W', 'info': 'I', 'trace': 'T',
            'debug': 'D'}`.
        child_class (Any): The class to be examined for acceptable class
            inheritance.
        *parent_classes (type): Variadic arguments containing all acceptable
            parent types for `child_classes`.  If any values of
            `child_classes` are not a valid type derived from one of
            `*parent_classes` then a log message will be emitted and a
            `TypeError` will be raised. Multiple parent_classes may be
            specified as separate arguments. If no parent_classes are
            specified, then a `RuntimeError` will be raised.
        allow_none (bool): If `True` then the values of `child_classes` are
            allowed to take on the value of `None` without causing the
            subclass check to fail.  If `False` (default) then `None` values
            will cause the subclass check to fail.

    Examples:
        # this will raise a `TypeError` because `Foo` is not `None` or
        # derived from Bar
        > class Bar: pass
        > class Foo: pass
        > error.subclass_check('<COR99962332E>', Bar, Foo=Foo)

        # this type check verifies that `foo` and `bar` are both strings
        > error.type_check('<COR03761101E>', str, foo=foo, bar=bar)
    """

    if allow_none and child_class is None:
        return

    if not parent_classes:
        raise RuntimeError(log_code, "invalid subclass check: no parent_classes given")

    if not isinstance(child_class, type) or not issubclass(
        child_class, parent_classes
    ):
        raise TypeError(log_code,
                "subclass check failed: {} is not a subclass of {}".format(
                    child_class,
                    parent_classes,
                )
            )


def value_check(log_code, condition, *args):
    """Check for acceptable values for a given object.  If this check fails, a log message will
    be emitted at the error level on the log channel associated with this handler and a
    `ValueError` exception will be raised with an appropriate message.  This check should be
    used for checking for appropriate values for variable instances.  For example, to check that
    a numerical value has an appropriate range.

    Args:
        log_code (str): A log code with format `<COR55705215E>` where `COR`
            is a short code for the library (for `caikit_core` in this
            example) and where `55705215` is a unique eight-digit identifier
            (example generation in `scripts/cor_log_code`) and where `E` is
            an error level short-code, one of `{'fatal': 'F', 'error': 'E',
            'warning': 'W', 'info': 'I', 'trace': 'T', 'debug': 'D'}`.
        condition (bool): A boolean value that should describe if this check
            passes `True` or fails `False`. Upon calling this function, this
            is typically provided as an expression, e.g., `0 < variable <
            1`.
        *args: A variable set of arguments describing the value check that failed. If no
            args are provided then an empty msg string is assumed and no additional
            information will be provided, otherwise the first argument will be treated as 'msg'
            argument. Note that string interpolation can be lazily performed on `msg` using `{}`
            format syntax by passing additional arguments.  This is the preferred method for
            performing string interpolation on `msg` so that it is only done if an error
            condition is encountered.

    """

    if not condition:
        interpolated_msg = (
            ""
            if not args
            else (args[0] if len(args) == 1 else args[0].format(*args[1:]))
        )

        raise ValueError(log_code, "value check failed: {}".format(interpolated_msg))

def file_check(log_code, *file_paths):
    """Check to see if one or more file paths exist and are regular files.  If any do not exist
    or are not files, then a log message will be emitted on the log channel associated with this
    error handler and a `FileNotFoundError` will be raised with an appropriate error message.

    Args:
        log_code (str): A log code with format `<COR73692990E>` where `COR`
            is a short code for the library (for `caikit_core` in this
            example) and where `55705215` is a unique eight-digit identifier
            (example generation in `scripts/cor_log_code`) and where `E` is
            an error level short-code, one of `{'fatal': 'F', 'error': 'E',
            'warning': 'W', 'info': 'I', 'trace': 'T', 'debug': 'D'}`.
        *file_paths (str): Variadic argument containing strings specifying
            the file paths to check.  If any of these file paths does not
            exist or is not a regular file, then a log message will be
            emitted and a `FileNotFoundError` will be raised.
    """

    for file_path in file_paths:
        if not os.path.exists(file_path):
            raise FileNotFoundError("File path `{}` does not exist".format(file_path))

        if not os.path.isfile(file_path):
            raise FileNotFoundError("Path `{}` is not a file".format(file_path))

def dir_check(log_code, *dir_paths):
    """Check to see if one or more directory paths exist and are, in fact, directories.  If any
    do not exist then a `FileNotFoundError` will be raised and if they are not directories then
    a `NotADirectoryError` will be raised.  In either case, a log message will be emitted on the
    log channel associated with this error handler.

    Args:
        log_code (str): A log code with format `<COR63462828E>` where `COR`
            is a short code for the library (for `caikit_core` in this
            example) and where `55705215` is a unique eight-digit identifier
            (example generation in `scripts/cor_log_code`) and where `E` is
            an error level short-code, one of `{'fatal': 'F', 'error': 'E',
            'warning': 'W', 'info': 'I', 'trace': 'T', 'debug': 'D'}`.
        *dir_paths (str): Variadic argument containing strings specifying
            the directory paths to check.  If any of these file paths does
            not exist or is not a regular file, then a log message will be
            emitted and a `FileNotFoundError` or `NotADirectoryError` will
            raised.
    """

    for dir_path in dir_paths:
        if not os.path.exists(dir_path):
            raise FileNotFoundError(log_code,
                    "Directory path `{}` does not exist".format(dir_path)
                )

        if not os.path.isdir(dir_path):
            raise NotADirectoryError(log_code, "Path `{}` is not a directory".format(dir_path))

def _fqname(o) -> str:
    try:
        class_ = o.__class__
        return ".".join([class_.__module__, class_.__qualname__])
    except Exception:  # pylint: disable=broad-exception-caught
        return str(type(o))
