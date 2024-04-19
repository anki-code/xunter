"""

This code was built on:
 * hunter.actions.CallPrinter
 * hunter.actions.StackPrinter
 * ProfileAction from https://python-hunter.readthedocs.io/en/latest/cookbook.html?highlight=depth_lt#profiling

"""

import os
import threading
from time import time
from collections import defaultdict
from itertools import islice
from hunter.util import CALL_COLORS, CODE_COLORS, MISSING, get_arguments, frame_iterator
from hunter.actions import CodePrinter, ColorStreamAction


class CallPrinterProfile(CodePrinter):
    """
    An action that just prints the code being executed, but unlike :obj:`hunter.CodePrinter` it indents based on
    callstack depth and it also shows ``repr()`` of function arguments.

    Args:
        stream (file-like): Stream to write to. Default: ``sys.stderr``.
        filename_alignment (int): Default size for the filename column (files are right-aligned). Default: ``40``.
        force_colors (bool): Force coloring. Default: ``False``.
        repr_limit (bool): Limit length of ``repr()`` output. Default: ``512``.
        repr_func (string or callable): Function to use instead of ``repr``.
            If string must be one of 'repr' or 'safe_repr'. Default: ``'safe_repr'``.

    .. versionadded:: 1.2.0
    """
    EVENT_COLORS = CALL_COLORS

    locals = defaultdict(list)
    overwrite_stream = None
    filter_time_sec_gt = None

    @classmethod
    def cleanup(cls):
        cls.locals = defaultdict(list)

    def __init__(self, *args, **kwargs):
        # <profile>
        self.timings = {}
        # </profile>

        if self.overwrite_stream:
            args['stream'] = self.overwrite_stream

        super(CallPrinterProfile, self).__init__(*args, **kwargs)

    def __call__(self, event):
        """
        Handle event and print filename, line number and source code. If event.kind is a `return` or `exception` also
        prints values.
        """
        ident = event.module, event.function

        thread = threading.current_thread()
        stack = self.locals[thread.ident]

        pid_prefix = self.pid_prefix()
        thread_prefix = self.thread_prefix(event)
        filename_prefix = self.filename_prefix(event)

        if event.kind == 'call':
            # <profile>
            self.timings[id(event.frame)] = time()
            # </profile>

            if event.builtin:
                self.output(
                    '{}{}{}{KIND}{:9} {}{COLOR} >{BUILTIN} {}.{}: {}{RESET}\n',
                    pid_prefix,
                    thread_prefix,
                    filename_prefix,
                    event.kind,
                    '   ' * (len(stack) - 1),
                    event.module,
                    event.function,
                    self.try_source(event).strip(),
                    COLOR=self.event_colors.get(event.kind),
                )
            else:
                code = event.code
                stack.append(ident)
                self.output(
                    '{}{}{}{KIND}{:9} {}{COLOR}=>{NORMAL} {}({}{COLOR}{NORMAL}){RESET}\n',
                    pid_prefix,
                    thread_prefix,
                    filename_prefix,
                    event.kind,
                    '   ' * (len(stack) - 1),
                    event.function,
                    ', '.join('{VARS}{0}{VARS-NAME}{1}{VARS}={RESET}{2}'.format(
                        prefix,
                        var_display,
                        self.try_str(event.locals.get(var_lookup, MISSING))
                        if event.detached
                        else self.try_repr(event.locals.get(var_lookup, MISSING)),
                        **self.other_colors
                    ) for prefix, var_lookup, var_display in get_arguments(code)),
                    COLOR=self.event_colors.get(event.kind),
                )
        elif event.kind == 'exception':
            if event.builtin:
                self.output(
                    '{}{}{}{KIND}{:9} {}{COLOR} ! {BUILTIN}{}.{}{RESET}\n',
                    pid_prefix,
                    thread_prefix,
                    filename_prefix,
                    event.kind,
                    '   ' * (len(stack) - 1),
                    event.module,
                    event.function,
                    COLOR=self.event_colors.get(event.kind),
                )
            else:
                self.output(
                    '{}{}{}{KIND}{:9} {}{COLOR} !{NORMAL} {}: {RESET}{}\n',
                    pid_prefix,
                    thread_prefix,
                    filename_prefix,
                    event.kind,
                    '   ' * (len(stack) - 1),
                    event.function,
                    self.try_str(event.arg) if event.detached else self.try_repr(event.arg),
                    COLOR=self.event_colors.get(event.kind),
                )
        elif event.kind == 'return':
            # <profile>
            start_time = self.timings.pop(id(event.frame), None)
            if start_time is None:
                return
            delta = time() - start_time
            timing_probe = f'time_sec=[{delta:.4f}]'  # + ' {event}'
            # </profile>

            if event.builtin:
                self.output(
                    '{}{}{}{KIND}{:9} {}{COLOR} <{BUILTIN} {}.{}{RESET} - {}\n',
                    pid_prefix,
                    thread_prefix,
                    filename_prefix,
                    event.kind,
                    '   ' * (len(stack) - 1),
                    event.module,
                    event.function,
                    timing_probe,
                    COLOR=self.event_colors.get(event.kind),
                )
            else:
                self.output(
                    '{}{}{}{KIND}{:9} {}{COLOR}<={NORMAL} {}{}{RESET}{} - {}\n',
                    pid_prefix,
                    thread_prefix,
                    filename_prefix,
                    event.kind,
                    '   ' * (len(stack) - 1),
                    event.function,
                    '' if event.builtin else ': ',
                    '' if event.builtin else (self.try_str(event.arg) if event.detached else self.try_repr(event.arg)),
                    timing_probe,
                    COLOR=self.event_colors.get(event.kind),
                )
                if stack and stack[-1] == ident:
                    stack.pop()
        else:
            if os.environ.get('XUNTER_SHOW_CODE', False):
                self.output(
                    '{}{}{}{KIND}{:9} {RESET}{}{}{RESET}\n',
                    pid_prefix,
                    thread_prefix,
                    filename_prefix,
                    event.kind,
                    '   ' * len(stack),
                    self.try_source(event).strip(),
                )

class StackPrinterProfile(ColorStreamAction):
    """
    An action that prints a one-line stacktrace.

    Args:
        depth (int): The maximum number of frames to show.
        limit (int): The maximum number of components to show in path. Eg: ``limit=2`` means it will show 1 parent: ``foo/bar.py``.
        stream (file-like): Stream to write to. Default: ``sys.stderr``.
        filename_alignment (int): Default size for the filename column (files are right-aligned). Default: ``40``.
        force_colors (bool): Force coloring. Default: ``False``.
        repr_limit (bool): Limit length of ``repr()`` output. Default: ``512``.
        repr_func (string or callable): Function to use instead of ``repr``.
            If string must be one of 'repr' or 'safe_repr'. Default: ``'safe_repr'``.
    """

    overwrite_stream = None
    filter_time_sec_gt = None

    def __init__(self, depth=15, limit=2, **options):
        self.limit = limit
        self.depth = depth
        # <profile>
        self.timings = {}
        # </profile>

        if self.overwrite_stream:
            options['stream'] = self.overwrite_stream

        super(StackPrinterProfile, self).__init__(**options)

    def __call__(self, event):
        """
        Handle event and print the stack.
        """
        pid_prefix = self.pid_prefix()
        thread_prefix = self.thread_prefix(event)
        filename_prefix = self.filename_prefix(event).rstrip()
        sep = os.path.sep

        if event.kind == 'call':
            # <profile>
            self.timings[id(event.frame)] = time()
            # </profile>
        elif event.kind == 'return':
            # <profile>
            start_time = self.timings.pop(id(event.frame), None)
            if start_time is None:
                return
            delta = time() - start_time
            timing_probe = f'time_sec=[{delta:.4f}]' # + ' {event}'
            # </profile>

        if event.frame and event.frame.f_back:
            template = '{}{}{}{CONT}:{BRIGHT}{fore(BLUE)}%s {KIND}<={RESET} %s' % (
                event.function,
                ' {KIND}<={RESET} '.join(
                    '%s{CONT}:{RESET}%s{CONT}:{BRIGHT}{fore(BLUE)}%s' % (
                        '/'.join(frame.f_code.co_filename.split(sep)[-self.limit:]),
                        frame.f_lineno,
                        frame.f_code.co_name
                    )
                    for frame in islice(frame_iterator(event.frame.f_back), self.depth)
                )
            )
        else:
            template = '{}{}{}{CONT}:{BRIGHT}{fore(BLUE)}%s {KIND}<= {BRIGHT}{fore(YELLOW)}no frames available {NORMAL}(detached=%s)' % (
                event.function,
                event.detached,
            )
        template += '{RESET}\n'
        if event.kind == 'return':
            if self.filter_time_sec_gt and delta < self.filter_time_sec_gt:
                return

            template = template.rstrip() + ' - {}\n'
            self.output(
                template,
                pid_prefix,
                thread_prefix,
                filename_prefix,
                timing_probe
            )
