""" searches the all (original) conll files in the directory 
    where it was called for the given string and creates a 
    subset conllu file with only the matching sentence objects.
    (This is primarily to be used for development purposes.)
    
    Output: This file is saved in it's on directory and named as follows: 
        'sample_{path_tag}/_{path_tag}_.conllu'
        where the path_tag is the search string with any spaces replaced with -
        e.g. `sample_the-few.conll/_the-few_.conllu`
        
    Note that previously created "sample_" directories are excluded
    from the search, and if the same exact search has been run
    previously (i.e. exact same search string) the prior output
    will be replaced with the new one. 
    """
from pathlib import Path
from sys import argv, exit

import pyconll

target_str = argv[1]
source = Path.cwd()
path_tag = target_str.replace(' ', '-')
outdir_stem = f'sample_{path_tag}'
outdir_end = '.conll'
outdir = source.joinpath(outdir_stem+outdir_end)

if outdir.is_dir():
    if list(outdir.iterdir()): 
        
        input_needed = True
        while input_needed:
            reply = input(f' ! >> {outdir.name} already exists--'
                        'Overwrite? [Y]/n\nInput: '
                        ).lower()
            
            if reply in 'yn':
                input_needed = False
                # (do nothing for 'y', 'Y', or '' reply)
                # exit script wihout changing anything
                if reply ==  'n':
                    exit('Prior conll subset will not be'
                        ' replaced. Quitting script.')
else:
    outdir.mkdir()
        
print(
    f'> Searching all (non-sample) .conllu files in {source} for sentences containing "{target_str}"...')

output = outdir.joinpath(f'_{path_tag}_.conllu')

outstrings = []
file_gen = (f for f in source.glob("**/*.conllu") 
         if not f.parent.name.startswith('sample'))

for f in file_gen:
    
    for c in pyconll.load.iter_from_file(f):

        conll_obj = c.conll()+'\n'

        if (f' {argv[1]} '.lower() in c.text.lower()
                and conll_obj not in outstrings):

            outstrings.append(conll_obj)

print(f'> Writing all matching sentences to:\n    {output}')
outtext = '\n'.join(outstrings)+'\n'
output.write_text(outtext)
print('Finished.')
