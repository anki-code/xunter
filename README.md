<p align="center">
<b>xunter</b> is to profiling <a href="https://xon.sh">xonsh shell</a> using <a href="https://github.com/ionelmc/python-hunter">hunter</a>. Time tracking is on board.
</p>

<p align="center">  
If you like the idea click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Trace%20xonsh%20shell%20code!&url=https://github.com/anki-code/xunter" target="_blank">tweet</a>.
</p>

## Install

Install xunter into the environment where xonsh you want to trace resides.

```xsh
pip install xunter
# or: pip install git+https://github.com/anki-code/xunter
```

## Usage

Xunter is working as drop-in replacement of `xonsh` with additional arguments:
```xsh
xonsh  --no-rc -c "2+2"
xunter --no-rc -c "2+2" ++depth-lt 5
#      ^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^
#            xonsh         xunter
```
Examples:
```xsh
xunter --no-rc -c "2+2" ++depth-lt 10
xunter --no-rc ++depth-lt 5 ++output /tmp/22.xunter
xunter --no-rc -c '2+2' ++filter 'Q(filename_endswith="main.py")'

xunter --no-rc -c 'echo 1' ++filter 'Q(filename_has="specs.py"),Q(function="run_subproc")'
# [...]/site-packages/xonsh/procs/specs.py:910:run_subproc 
#   <= xonsh/built_ins.py:206:subproc_captured_hiddenobject 
#   <= <string>:1:<module> <= xonsh/codecache.py:64:run_compiled_code 
#   <= xonsh/codecache.py:218:run_code_with_cache
#   <= xonsh/main.py:519:main_xonsh 
#   <= xonsh/main.py:470:main 
#   <= xunter/xunter:91:<module>
#   - time_sec=[0.1505]

# Don't forget about xonsh`s awesome macro call:
xunter --no-rc -c 'echo 1' ++filter! Q(filename_has="specs.py"),Q(function="run_subproc")
```
To set `++filter` read about [filters](https://python-hunter.readthedocs.io/en/latest/filtering.html) 
and take a look into the [cookbook](https://python-hunter.readthedocs.io/en/latest/cookbook.html).
Use `./playground/trace.py` to experiment with the tracing filters and understand how it works.

## Convert log to table

```python
xunter --no-rc -c "2+2" ++depth-lt 10 ++printer stack ++output /tmp/22.xunter
xunter2excel /tmp/22.xunter
```

## Known issues

If you see the unexpected exceptions try to install xonsh from the main branch first.

## See also
* [xonsh-cheatsheet](https://github.com/anki-code/xonsh-cheatsheet)
* [xonsh-install](https://github.com/anki-code/xonsh-install)
* By putting `import ipdb; ipdb.set_trace()` into any place of code you can investigate the environment interactively.
