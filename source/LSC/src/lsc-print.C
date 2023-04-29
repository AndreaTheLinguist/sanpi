
/*MA****************************************************************/
/*                                                                 */
/*  FILE     lsc-print.C                                           */
/*  MODULE   lsc-print                                             */
/*  PROGRAM  lsc                                                   */
/*  AUTHOR   Helmut Schmid, IMS, University of Stuttgart           */
/*                                                                 */
/*  PURPOSE  Latent Semantic Clustering                            */
/*                                                                 */
/*ME****************************************************************/

#include <iostream>
using std::cout;

#include "lsc.h"


/*FA****************************************************************/
/*                                                                 */
/*  usage                                                          */
/*                                                                 */
/*FE****************************************************************/

void usage()

{
  cerr << "\nUsage: lsc-print [options] [file]\n\nOptions:\n\n-n f\tPrint n many words for each feature of a cluster (default 10).\n\n";
  exit(1);
}


/*FA****************************************************************/
/*                                                                 */
/*  main                                                           */
/*                                                                 */
/*FE****************************************************************/

int main( int argc, char **argv )

{
  FILE *parfile;
  int  no_of_words=10;

  while (argc > 1 && argv[1][0] == '-') {
    int n=0;
    if (strcmp(argv[1], "-h") == 0) {
      usage();
    }
    else if (argc > 2) {
      if (strcmp(argv[1], "-n") == 0) {
	no_of_words = atoi(argv[2]);
	if (no_of_words < 0)
	  usage();
      }
      else
	break;
      n++;
    }
    else
      break;
    n++;
    argc -= n;
    for( int i=1; i<argc; i++ )
      argv[i] = argv[i+n];
  }

  if (argc > 1) {
    if ((parfile = fopen(argv[1], "rb")) == NULL) {
      cerr << "Error: Cannot open parameter file " << argv[1] << "!\n";
      exit(1);
    }
  }
  else
    parfile = stdin;


  try {
    LSC model;
    model.read( parfile );
    model.print( cout, no_of_words );
  }
  catch (const char *message) {
    cerr << "Error: " << message << "\n";
    exit(1);
  }
}
