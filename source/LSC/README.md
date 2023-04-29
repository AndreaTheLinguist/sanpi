# LSC
The LSC model is a soft-clustering model for n-tuples of words,
e.g. for verb-object pairs or for verb-preposition-noun triples. The
model is described in a paper by Mats Rooth entitled "Two-dimensional
clusters in grammatical relations" which is available at
[http://www.ims.uni-stuttgart.de/~mats](http://www.ims.uni-stuttgart.de/~mats)

The LSC model is trained with the following command

```{shell}
$ src/lsc-train 20 50 data/vo.txt > data/m-20-50
```

Arguments:

1. number of clusters.
2. number of EM training iterations.
3. name of the file with the training data.\
   ⫯ `LSC/data/vo.txt` contains sample training data.

The first line of the data file contains the number of elements in
each tuple (2 for pairs, 3 for triples etc.) 
Each of the following lines contains one data item consisting of 
the tuple frequency and the words of the data tuple. 
Tabs are used as field separators.

The LSC model is stored as a binary file. The following command will
print it in readable form:

```{shell}
$ src/lsc-print -n 10 data/m-20-50 > data/m-20-50.txt
```

The program lsc-disambiguate can be used to evaluate the model on a
pseudo disambiguation task.

```{shell}
$ src/lsc-disambiguate data/m-20-50 data/vo-test.txt
```

©️ Helmut Schmid, IMS, University of Stuttgart

Any comments or bug reports should be sent to
schmid@ims.uni-stuttgart.de
