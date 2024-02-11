To use `ucs-make-tables` I wrote a quick script to print out all the pairs from a directory of filled json files and then pipe it into the UCS tool.

The script is `script/print_adv_adj.py` and is as follows: 

```python
import sys
import json
import os
from pathlib import Path

json_dir = Path.cwd()/sys.argv[1]

if not json_dir.is_dir():

    sys.exit('Error: Specified json directory does not '
             'exist.')

errors = 0

for f in os.scandir(json_dir):

    if f.name.endswith('json') and not f.name.endswith('raw.json'):

        with open(f, 'r') as j:

            for hit in json.load(j):

                nodes = hit['matching']['fillers']

                pair = (nodes['ADV'] + '\t' +
                        nodes['ADJ'])

                try:

                    print(pair)

                except UnicodeError:

                    error += 1
                    print(f"Encoding error. Pair {pair} skipped.")

            # print(f'{errors} errors in {f.name}')
```


I used it like this, where `-f` indicates frequency threshold, and `-v` indicates a verbose output: 

```shell
andrea@Delilah:~/litotes$ python script/print_adv_adj.py Nyt1.posBe_x_not/ | ucs-make-tables -v -f 5 posBe_x_not_thresh5.ds.gz
N =   751655,  V = 100895
Saving to posBe_x_not_thresh5.ds.gz ...done
andrea@Delilah:~/litotes$ ucs-print -i posBe_x_not_thresh5.ds.gz | head -20
id            l1  l2              f     f1     f2       N
--  ------------  ------------  ---  -----  -----  ------
1          that  easy          219   4551   5730  751655
2  particularly  pervasive       5  13300    285  751655
3         fully  privatized      5   2301      8  751655
4            so  candid          9  87353    307  751655
5       totally  weird          13   4844    474  751655
6        almost  tender         28   9738    265  751655
7  increasingly  relevant        7   3689    414  751655
8      probably  familiar       21   4117   1328  751655
9            as  miraculous     22  47941     58  751655
10            as  inaccurate      7  47941    175  751655
11        easily  worth          13    778   3044  751655
12          well  informed        6   2933    107  751655
13    absolutely  incredible     44   5379    428  751655
14          also  right          90  24962   4525  751655
15          very  brave          95  95764    230  751655
16        rather  good           25   2154  19810  751655
17        mostly  flat           18   2582    736  751655
18           too  robust         26  62682    464  751655  
```

Then I used `ucs-add` and `ucs-sort` to add association scores (t scores and log likelihood) and then sort by log likelihood (it looks cleaner than this in the terminal):

```shell
andrea@Delilah:~/litotes$ ucs-add -v am.t.score am.log.likelihood TO posBe_x_not_thresh5.ds.gz INTO posBe_thresh5_scores.ds.gz   
Variables: id, l1, l2, f, f1, f2, N
Adding: am.t.score, am.log.likelihood
Processing complete (19830 rows).
andrea@Delilah:~/litotes$ ucs-sort posBe_thresh5_scores.ds.gz by am.log.likelihood | ucs-print -i | head -20

id                    l1  l2                       f     f1     f2       N     am.t.score  am.log.likelihood
-----  --------------------  --------------------  ----  -----  -----  ------  -------------  -----------------
8427                barely  distinguishable       1834   2906   1864  751655    42.65694978      21595.8021472
7739                   too  late                  4075  62682   4524  751655    57.92578651      17641.9307351
11630                   too  early                 4028  62682   4560  751655    57.47490462      17057.3497745
2811                    no  different             2177   4010  11523  751655    45.34079756      13140.9306003
14589                  well  aware                 1572   2933   4619  751655    39.19387010      12575.3206864
19380                 still  alive                 2169  26869   2538  751655    44.62449789      12545.0191343
2977                  also  available             3142  24962   8851  751655    50.80969802      10620.9081995
3048                   all  right                 1697   6670   4525  751655    40.21992847      10555.9684909
3214                  long  overdue                738   1057    803  751655    27.12458888       9952.2607590
12526                almost  impossible            1563   9738   4308  751655    38.12307851       8265.2071075
18927                   too  much                  3250  62682   6550  751655    47.42748283       7772.2583599
18413                almost  certain               1193   9738   2407  751655    33.63699978       7211.9555345
4810                   now  available             1681  10440   8851  751655    38.00159404       6224.9289321
833                   too  busy                  2223  62682   4082  751655    39.92886110       5804.7605984
9039                  very  difficult             4136  95764   9379  751655    45.73155730       5707.2864351
9142                  just  fine                   916  13338   1452  751655    29.41417542       5554.8935194
10512                highly  unlikely               824   6461   1806  751655    28.16460187       5472.6652609
15231                nearly  impossible             869   3193   4308  751655    28.85801386       5441.6951553

```

`ucs-add` to add ranks for included association scores: 

```shell
andrea@Delilah:~/litotes$ ucs-add -v 'r.%' TO posBe_thresh5_scores.ds.gz INTO posBe_thresh5_ranks.ds.gz
[activating memory mode to add rankings]
Loading data set posBe_thresh5_scores.ds.gz ... 19830 rows
Data set variables: id l1 l2 f f1 f2 N am.t.score am.log.likelihood
Adding variables:   r.t.score r.log.likelihood
Writing data set to posBe_thresh5_ranks.ds.gz ... done
```

and `ucs-sort` again to sort by t score rank to compare with log likelihood ranks:

```shell
ucs-sort posBe_thresh5_ranks.ds.gz by am.t.score | ucs-print -i 'r.%' '*' from - | head -20 

r.t.score  r.log.likelihood     id                    l1  l2                       f     f1     f2       N
---------  ----------------  -----  --------------------  --------------------  ----  -----  -----  ------
1                 2   7739                   too  late                  4075  62682   4524  751655
2                 3  11630                   too  early                 4028  62682   4560  751655
3                 7   2977                  also  available             3142  24962   8851  751655
4                11  18927                   too  much                  3250  62682   6550  751655
5                15   9039                  very  difficult             4136  95764   9379  751655
6                 4   2811                    no  different             2177   4010  11523  751655
7                 6  19380                 still  alive                 2169  26869   2538  751655
8                 1   8427                barely  distinguishable       1834   2906   1864  751655
9                26  15241                  very  important             4460  95764  13452  751655
10                 8   3048                   all  right                 1697   6670   4525  751655
11                14    833                   too  busy                  2223  62682   4082  751655
12                32   3326                    as  good                  3688  47941  19810  751655
13                 5  14589                  well  aware                 1572   2933   4619  751655
14                10  12526                almost  impossible            1563   9738   4308  751655
15                13   4810                   now  available             1681  10440   8851  751655
16                33  17570                   too  high                  2751  62682   9434  751655
17                27   3506                pretty  good                  2281  19277  19810  751655
18                34   4321                   too  small                 1953  62682   5224  751655
```