
/*MA****************************************************************/
/*                                                                 */
/*  FILE     lsc-train.C                                           */
/*  MODULE   lsc-train                                             */
/*  PROGRAM  lsc                                                   */
/*  AUTHOR   Helmut Schmid, IMS, University of Stuttgart           */
/*                                                                 */
/*  PURPOSE  Latent Semantic Clustering                            */
/*                                                                 */
/*ME****************************************************************/

#include "lsc.h"


/*FA****************************************************************/
/*                                                                 */
/*  usage                                                          */
/*                                                                 */
/*FE****************************************************************/

void usage()

{
  cerr << "\nUsage: lsc-train [options] #clusters #iterations infile outfile\n\nOptions:\n\n-s n\tUse n as seed for random number generator\n\n";
  exit(1);
}


/*FA****************************************************************/
/*                                                                 */
/*  main                                                           */
/*                                                                 */
/*FE****************************************************************/

int main( int argc, char **argv )

{
  int noc;
  int noi;
  int seed=1;
  FILE *infile;
  FILE *outfile;

  while (argc > 1 && argv[1][0] == '-') {
    int n=0;
    if (strcmp(argv[1], "-h") == 0) {
      usage();
    }
    else if (argc > 2) {
      if (strcmp(argv[1], "-s") == 0) {
	seed = atoi(argv[2]);
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

  if (argc > 2) {
    noc = atoi(argv[1]);
    if (noc < 1) {
      cerr << "invalid number of clusters: " << noc << "\n";
      usage();
    }
    noi = atoi(argv[2]);
    if (noi < 0) {
      cerr << "invalid number of iterations: " << noi << "\n";
      usage();
    }
  }
  else
    usage();

  if (argc > 3) {
    if ((infile = fopen(argv[3], "rt")) == NULL) {
      cerr << "Error: Cannot open input file " << argv[3] << "!\n";
      exit(1);
    }
  }
  else
    usage();

  if (argc > 4) {
    if ((outfile = fopen(argv[4], "wt")) == NULL) {
      fprintf(stderr, "Error: Cannot open output file %s!\n", argv[4]);
      exit(1);
    }
  }
  else
    outfile = stdout;

  try {
    LSC model(infile, noc);
    model.init(seed);
    model.train( noi );
    model.store( outfile );
  }
  catch (const char *message) {
    cerr << "Error: " << message << "\naborted\n";
    exit(1);
  }
}
