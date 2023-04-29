
/*MA****************************************************************/
/*                                                                 */
/*  FILE     lsc-disambiguate.C                                    */
/*  MODULE   lsc-disambiguate                                      */
/*  PROGRAM  lsc                                                   */
/*  AUTHOR   Helmut Schmid, IMS, University of Stuttgart           */
/*                                                                 */
/*  PURPOSE  Latent Semantic Clustering                            */
/*                                                                 */
/*ME****************************************************************/

#include "lsc.h"

#include <iostream>
using std::cout;


/*FA****************************************************************/
/*                                                                 */
/*  main                                                           */
/*                                                                 */
/*FE****************************************************************/

int main( int argc, char **argv )

{
  FILE *parfile;
  FILE *infile;
  FILE *outfile;

  if (argc > 1) {
    if ((parfile = fopen(argv[1], "rb")) == NULL) {
      cerr << "Error: Cannot open parameter file " << argv[1] << "!\n";
      exit(1);
    }
  }
  else {
    cerr << "\nUsage: lsc-disambiguate parfile infile outfile\n\n";
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

  if (argc > 3) {
    if ((outfile = fopen(argv[3], "wt")) == NULL) {
      fprintf(stderr, "Error: Cannot open output file %s!\n", argv[3]);
      exit(1);
    }
  }
  else
    outfile = stdout;

  try {
    LSC model;
    model.read( parfile );

    char buffer[1000];
    long correct=0;
    long wrong=0;
    long others=0;
    for( int i=1; fgets(buffer, 1000, infile); i++) {
      char *w1 = strtok(buffer, "\t\n");
      char *w2 = strtok(NULL, "\t\n");
      char *w3 = strtok(NULL, "\t\n");
      if (w3 == NULL) {
	cerr << "Error in line " << i << "\n";
	exit(1);
      }
      double p1=model.prob( w1, w2 );
      double p2=model.prob( w3, w2 );
      if (p1 > p2) {
	fputs("1", outfile);
	correct++;
      }
      else if (p1 < p2) {
	fputs("-1", outfile);
	wrong++;
      }
      else {
	fputs("0", outfile);
	others++;
      }
      fprintf(outfile, "\t%s\t%s\t%s\n", w1, w2, w3);
    }
    double accuracy = 100.0 * ((double)correct + (double)others * 0.5) /
      (double)(correct + wrong + others);
    cout << "correct:\t" << correct << "\n";
    cout << "wrong:\t" << wrong << "\n";
    cout << "don't know:\t" << others << "\n";
    cout << "accuracy:\t" << accuracy << "\n";
  }
  catch (const char *message) {
    cerr << "Error: " << message << "\n";
    exit(1);
  }
}
