<p align="center">
<b>xunter</b> is to profiling <a href="https://xon.sh">the xonsh shell</a> using <a href="https://github.com/ionelmc/python-hunter">hunter</a>.
</p>

<p align="center">  
If you like the idea click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Nice%20prompt%20for%20the%20xonsh%20shell!&url=https://github.com/anki-code/xontrib-xontrib-prompt-starship" target="_blank">tweet</a>.
</p>

## Install

Install xunter into the environment where xonsh you want to trace resides.

```xsh
pip install git+https://github.com/anki-code/xunter
```

## Usage

Xunter is working as drop-in replacement of `xonsh` with additional arguments:
```xsh
xunter --help
xunter --no-rc -c "2+2" ++depth-lt 5
#      ^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^
#            xonsh         xunter
```

## Convert log to table

```python
xunter --no-rc -c "2+2" ++depth 10 ++output /tmp/22.xunter
xunter2excel /tmp/22.xunter
```

## Investigations

By putting `import ipdb; ipdb.set_trace()` in the any place of code you can investigate the environment interactively.

## Known issues

If you see the unexpected exceptions try to install xonsh from the main branch first.

## See also

* [xonsh-install](https://github.com/anki-code/xonsh-install)