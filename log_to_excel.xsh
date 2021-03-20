import pandas as pd

stack_log_file = $ARG1

if not fp'{stack_log_file}'.exists():
    printx('{YELLOW}File not found{RESET}')
    exit(1)

lines = []
times = []
with open(stack_log_file) as f:
    for l in f:
        stack, time = l.split(' - ')
        lines.append(['0'] + stack.split(' <= ')[::-1])
        times.append(time[10:-2])

df = pd.DataFrame(lines)
df[0] = times
df[0] = df[0].apply(float)
stack_log_file_xlsx = stack_log_file + '.xlsx'
df.to_excel(stack_log_file_xlsx)
printx(f'{{GREEN}}Saved to {stack_log_file_xlsx}')