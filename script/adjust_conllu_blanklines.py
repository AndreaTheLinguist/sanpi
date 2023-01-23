from pathlib import Path
from sys import argv
import time

#// tmp = Path('/share/compling/projects/sanpi/playground/adjusted_conllus/tmp.txt')
#// if not tmp.parent.is_dir():
#//     tmp.parent.mkdir(parents=True)
NEW_LINE_REQ = 2
check_dir = Path(argv[1]).resolve()
log_path = check_dir.joinpath(
    f'eof-blanks-adjust_{time.strftime("%Y-%m-%d_%R")}.log')
log_lines = [f'Adjusting blank lines at end of conllu files in {check_dir}',
             time.strftime("%Y-%m-%d @ %I:%M%p")]
print(f'Adjusting blank lines at end of conllu files in {check_dir}...')
for p in Path(check_dir).rglob('*conllu'):
    log_line = ''
    nlcount = p.read_text()[-15:].count('\n')
    if nlcount > NEW_LINE_REQ or nlcount < NEW_LINE_REQ:
        text = p.read_text(encoding='utf8')

        while text[-15:].count('\n') > NEW_LINE_REQ:
            #    text.endswith('\n'*4)
            text = text[:-1]

        # while text.endswith(('\n'*2, '\n'*1)) or not text.endswith('\n'):
        while text[-15:].count('\n') < NEW_LINE_REQ:
            text += '\n'

        if text.endswith('\n'*NEW_LINE_REQ) and not text.endswith('\n'*(NEW_LINE_REQ + 1)):
            #// tmp.with_name(p.name).write_text(text, encoding='utf8')
            p.write_text(text, encoding='utf8')
            log_line = f'{p.stem} ✔'
        
        else: 
            log_line = f'ERROR. Check {p.relative_to(check_dir)}.'

    else:
        log_line = f'(No adjustment needed for {p.stem})'
    
    # print(log_line)
    log_lines.append(log_line)

log_lines.append(f'Finished: {time.strftime("%Y-%m-%d @ %I:%M%p")}')
log_path.write_text('\n'.join(log_lines), encoding='utf8')        
print(f'✔ Finished.\n  Log saved to {log_path.relative_to(check_dir)}')
