    """searches the entire directory (where it was called) for the given string and creates a subset conllu file with only matching sentences. (This is
    primarily to be used for development purposes.)
    
    Output: This file is saved in it's on directory and named as follows: 
        'sample_{path_tag}/_{path_tag}_.conllu'
        where the path_tag is the search string with any spaces replaced with -
        e.g. `sample_the-few.conll/_the-few_.conllu`
    """
import pyconll
from pathlib import Path
from sys import argv

target_str = argv[1]
source = Path.cwd()
print(
    f'> Searching all .conllu files in {source} for sentences containing "{target_str}"...')

path_tag = target_str.replace(' ', '-')
outdir = source.joinpath(f'sample_{path_tag}.conll')

if not outdir.is_dir():
    outdir.mkdir()

output = outdir.joinpath(f'_{path_tag}_.conllu')

outstrings = []
files = source.glob("**/*.conllu")
for f in files:

    for c in pyconll.load.iter_from_file(f):

        conll_obj = c.conll()+'\n'

        if (f' {argv[1]} '.lower() in c.text.lower()
                and conll_obj not in outstrings):

            outstrings.append(conll_obj)

print(f'> Writing all matching sentences to:\n    {output}')
outtext = '\n'.join(outstrings)+'\n'
output.write_text(outtext)
print('Finished.')
