# coding=utf-8

from pathlib import Path
from pprint import pprint
import re
from sys import argv
from textwrap import indent
from source.utils.general import confirm_dir, TEX_ASSETS, snake_to_camel
# REDO = argv[-1] if len(argv) > 1 else True

TEST = False


def _main():
    for tex_path in Path.home().joinpath('justwriting/assets/parses').glob('*.tex'):
        if 'dep-tree' in tex_path.name:
            continue
        position = int(Path(tex_path.stem).suffix.strip('.'))
        init_info = Path(tex_path.stem).stem.replace('BIGRAM.', 'BIGRAM_', 1)

        # if strip_path.is_file() and not REDO:
        #     continue

        print(tex_path)
        print('\n~~~~~~~~~~~~~~\n')

        body = tex_path.read_text()
        adv_color = 'DarkOrchid'
        adj_color = 'Emerald'
        
        dep_tree = re.search(r'\\begin\{dependency\}.+\\end\{dependency\}',
                             body.replace('\n', 'NEWLINE')
                             ).group().replace('NEWLINE', '\n')
        # dep_lines = re.findall(r'[^\n]+[\\\{][d&][^o].+\n', body)
        # dep_tree = ''.join(dep_lines)
        dep_tree = re.sub(r'(?<=\s)[A-Z]*,([A-Z]{2,} )', r'\1 ', dep_tree)
        dep_tree = re.sub(r'RB\w?', 
                          '\\\\cmtt{\\\\textcolor{'+adv_color+'}{ADV}}', dep_tree)
        dep_tree = re.sub(r'JJ\w?', 
                          '\\\\cmtt{\\\\textcolor{'+adj_color+'}{ADJ}}', dep_tree)
        dep_tree = re.sub(r'[A-Z]{2,}\s*(\\[\\&])', r'\1', dep_tree)
        dep_tree = re.sub(r'(\d\}\{)([a-zA-Z:]+)(\}\n)', 
                          r'\1\\cmtt{\2}\3',
                          dep_tree)
        dep_tree = f'\\footnotesize\n{dep_tree}\n\\normalsize'
        print(indent(dep_tree, prefix='  '))
        
        sent_label = snake_to_camel(
            re.sub(r'\W+', '_',
                   re.search(r'\t.*& [a-z].*\\', dep_tree
                             ).group()
                   ))
        strip_path = TEX_ASSETS.joinpath('deps').joinpath(
            f'{init_info}/{position}_{sent_label}').with_suffix('.dep-tree.tex')
        confirm_dir(strip_path.parent)
        strip_path.write_text(dep_tree)
        print(f'stripped latex dependency tree saved as\n  {strip_path}')
        print('***')
        print(indent(dep_tree, prefix='\t'))
        print('***\n')
        if TEST:
            break


if __name__ == '__main__':
    _main()
