Profiling for the xonsh shell based on hunter.
<p align="center">
<b>xunter<b> - profiling for <a href="https://xon.sh">the xonsh shell</a> based on <a href="https://github.com/ionelmc/python-hunter">hunter</a>.
</p>

<p align="center">  
If you like the idea click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Nice%20prompt%20for%20the%20xonsh%20shell!&url=https://github.com/anki-code/xontrib-xontrib-prompt-starship" target="_blank">tweet</a>.
</p>

## Install

```python
git clone https://github.com/anki-code/xunter 
cd xunter
pip install -r requirements.txt
```

## Usage

Run profiling:
```python
$XUNTER_PRINTER='stack' $XUNTER_DEPTH_LT=5 $XUNTER_MIN_SEC=1.5 $XONSH_DEBUG=1 python profile_xonsh.py --no-rc -c "print('Catch Me If You Can')"
$XUNTER_PRINTER='call' $XUNTER_DEPTH_LT=5 $XONSH_DEBUG=1 python profile_xonsh.py --no-rc -c "print('Catch Me If You Can')"
```

## Environment variables

* `XUNTER_PRINTER` - `stack` or `call`. Default `stack`.
* `XUNTER_DEPTH_LT` - Maximum depth of call stack. Default `5`. 

Stack printer:
* `XUNTER_MIN_SEC` - Minimal amount of function execution time in seconds to show call stack. Default `0.0`.

Call printer:
* `XUNTER_SHOW_CODE` - Show function code. Default `False`.

## Playground

```python
$XUNTER_DEPTH_LT=5 python profile_playground.py
```

## Log to excel

```python
$XUNTER_PRINTER='stack' $XUNTER_DEPTH_LT=20 $XONSH_DEBUG=1 python profile_xonsh.py --no-rc -c "print(123)" e> /tmp/xunter.log
log_to_excel.py /tmp/xunter.log
xdg-open /tmp/xunter.log.xlsx
```

