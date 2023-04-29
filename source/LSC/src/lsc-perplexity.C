
/*MA****************************************************************/
/*                                                                 */
/*  FILE     lsc-perplexity.C                                      */
/*  MODULE   lsc-perplexity                                        */
/*  PROGRAM  lsc                                                   */
/*  AUTHOR   Helmut Schmid, IMS, University of Stuttgart           */
/*                                                                 */
/*  PURPOSE  Latent Semantic Clustering                            */
/*                                                                 */
/*ME****************************************************************/

#include <iostream>
using std::cout;

#include <math.h>

#include "lsc.h"


/*FA****************************************************************/
/*                                                                 */
/*  main                                                           */
/*                                                                 */
/*FE****************************************************************/

int main( int argc, char **argv )

{
  FILE *parfile;
  FILE *infile;

  if (argc > 1) {
    if ((parfile = fopen(argv[1], "rb")) == NULL) {
      cerr << "Error: Cannot open parameter file " << argv[1] << "!\n";
      exit(1);
    }
  }
  else {
    cerr << "\nUsage: lsc-perplexity parfile infile\n\n";
    exit(1);
  }

  if (argc > 2) {
    if ((infile = fopen(argv[2], "rt")) == NULL) {
      cerr << "Error: Cannot open input file " << argv[2] << "!\n";
      exit(1);
    }
  }
  else
    infile = stdin;

  try {
    LSC model;
    model.read( parfile );

    char buffer[1000];
    long n=0;
    long found=0;
    double lp=0.0;
    for( int i=0; fgets(buffer, 1000, infile); i++) {
      long f = atol(strtok(buffer, "\t\n"));
      char *w1 = strtok(NULL, "\t\n");
      char *w2 = strtok(NULL, "\t\n");
      if (w2 == NULL) {
	cerr << "Error in line " << i << "\n";
	exit(1);
      }
      double p=model.prob( w1, w2 );
      n += f;
      if (p > 0.0) {
	lp += log(p) * (double)f;
	found += f;
      }
    }
    cout << "perplexity:\t" << exp(-lp/(double)found) << "\n";
    cout << "found:\t" << found << "\n";
    cout << "total:\t" << n << "\n";
  }
  catch (const char *message) {
    cerr << "Error: " << message << "\n";
    exit(1);
  }
}
