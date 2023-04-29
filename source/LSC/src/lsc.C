
/*MA****************************************************************/
/*                                                                 */
/*  FILE     lsc.C                                                 */
/*  MODULE   lsc                                                   */
/*  PROGRAM  lsc                                                   */
/*  AUTHOR   Helmut Schmid, IMS, University of Stuttgart           */
/*                                                                 */
/*  PURPOSE  Latent Semantic Clustering                            */
/*                                                                 */
/*ME****************************************************************/

#include <math.h>

#include "lsc.h"

int const BUFFER_SIZE=1000;


/*FA****************************************************************/
/*                                                                 */
/*  error_at_line                                                  */
/*                                                                 */
/*FE****************************************************************/

void error_at_line( long line_no, char *line )

{
  char message[BUFFER_SIZE+100];
  sprintf( message, "in input file at line %ld:\n%s", line_no, line);
  throw message;
}


/*FA****************************************************************/
/*                                                                 */
/*  LSC::estimate_probs                                            */
/*                                                                 */
/*FE****************************************************************/

void LSC::estimate_probs()

{
  {
    double sum=0.0;
    
    for( int c=0; c<noc; c++)
      sum += cluster_freq[c];
    for( int c=0; c<noc; c++) {
      cluster_prob[c] = (float)(cluster_freq[c] / sum);
      cluster_freq[c] = 0.0;
    }
  }

  for( int c=0; c<noc; c++)
    for( int f=0; f<nof; f++) {
      double sum = 0.0;
      for( long w=0; w<feature[f].size(); w++)
	sum += feature_freq[c][f][w];
      double fac = 1.0/sum;
      for( long w=0; w<feature[f].size(); w++) {
	feature_prob[c][f][w] = (float)(feature_freq[c][f][w] * fac);
	feature_freq[c][f][w] = 0.0;
      }
    }
}


/*FA****************************************************************/
/*                                                                 */
/*  LSC::estimate_freqs                                            */
/*                                                                 */
/*FE****************************************************************/

void LSC::estimate_freqs()

{
  double *p=new double[noc];

  for( long d=0; d<data_size; d++)
    if (data[d].cluster == -1) {
      double sum=0.0;
      for( int c=0; c<noc; c++) {
	p[c] = cluster_prob[c];
	for( int f=0; f<nof; f++)
	  p[c] *= feature_prob[c][f][data[d].feature[f]];
	sum += p[c];
      }
      double fac = data[d].freq/sum;
      for( int c=0; c<noc; c++) {
	double freq = p[c] * fac;
	cluster_freq[c] += freq;
	for( int f=0; f<nof; f++)
	  feature_freq[c][f][data[d].feature[f]] += freq;
      }
    }
    else {
      cluster_freq[data[d].cluster] += data[d].freq;
      for( int f=0; f<nof; f++)
	feature_freq[data[d].cluster][f][data[d].feature[f]] += data[d].freq;
    }
  delete[] p;
}


/*FA****************************************************************/
/*                                                                 */
/*  LSC::init                                                      */
/*                                                                 */
/*FE****************************************************************/

void LSC::init( int seed )

{
  srand(seed);
  for( int c=0; c<noc; c++)
    cluster_freq[c] = 1.0;
  for( int c=0; c<noc; c++)
    for( int f=0; f<nof; f++)
      for( long w=0; w<feature[f].size(); w++)
	feature_freq[c][f][w] = 1.0+rand()/(double)RAND_MAX;
  estimate_probs();
}


/*FA****************************************************************/
/*                                                                 */
/*  LSC::LSC                                                       */
/*                                                                 */
/*FE****************************************************************/

LSC::LSC( FILE *file, int c )

{
  char buffer[BUFFER_SIZE];

  if (file == stdin)
    throw "It is not possible to read LSC data from stdin!";
  quiet = 0;
  long n=0;
  noc = c;

  for( n=0; fgets(buffer, BUFFER_SIZE, file); n++);
  rewind(file);
  data_size = n-1;

  // read the number of features
  char *s=fgets(buffer, BUFFER_SIZE, file);
  int end;
  if (s == NULL || sscanf(buffer,"%d %n", &nof, &end) != 1 || 
      buffer[end] != '\0')
    error_at_line(1, buffer);

  // memory allocation
  feature = new Feature[nof];
  data = new Data[data_size];

  // read the data vectors
  for( n=0; fgets(buffer, BUFFER_SIZE, file); n++ ) {
    if (buffer[0] == '\n')
      continue;

    data[n].feature = new FNo[nof];

    // read the frequency
    {
      double f;
      if (sscanf(buffer, "%lf %n", &f, &end) != 1)
	error_at_line(n+2, buffer);
      data[n].freq = f;
    }

    // read the features
    for( int i=0; i<nof; i++ ) {
      if (i == 0)
	s = strtok(buffer+end, "\t\n");
      else
	s = strtok(NULL, "\t\n");
      if (s == NULL)
	error_at_line(n+2, buffer);
      data[n].feature[i] = feature[i].insert(s);
    }
    // read an optional cluster assignment
    if ((s = strtok(NULL, "\t\n"))) {
      if (sscanf(s,"%hd",&data[n].cluster) != 1 ||
	  data[n].cluster < 0 || data[n].cluster >= noc)
	error_at_line(n+2, buffer);
    }
    else
      data[n].cluster = -1;
  }

  // memory allocation
  cluster_prob = new float[noc];
  cluster_freq = new Freq[noc];
  feature_prob = new float**[noc];
  feature_freq = new Freq**[noc];
  for( int i=0; i<noc; i++ ) {
    feature_prob[i] = new float*[nof];
    feature_freq[i] = new Freq*[nof];
    for( int k=0; k<nof; k++ ) {
      feature_prob[i][k] = new float[feature[k].size()];
      feature_freq[i][k] = new Freq[feature[k].size()];
    }
  }

  init();
}


/*FA****************************************************************/
/*                                                                 */
/*  LSC::~LSC                                                      */
/*                                                                 */
/*FE****************************************************************/

LSC::~LSC()

{
  delete[] feature; 
  delete[] data;
  delete[] cluster_prob; 
  delete[] cluster_freq; 
  for( int i=0; i<noc; i++ ) {
    for( int k=0; k<nof; k++ ) {
      delete[] feature_prob[i][k];
      if (feature_freq != NULL)
	delete[] feature_freq[i][k];
    }
    delete[] feature_prob[i];
    if (feature_freq != NULL)
      delete[] feature_freq[i];
  }
  delete[] feature_prob; 
  delete[] feature_freq; 
}


/*FA****************************************************************/
/*                                                                 */
/*  sort_probs                                                     */
/*                                                                 */
/*FE****************************************************************/

static long sort_probs( FP *fp, long n, float *prob )

{
  long i,k=0;
  for( i=0; i<n; i++)
    if (prob[i] > 0.0) {
      fp[k].number = i;
      fp[k++].prob = prob[i];
    }
  sort(fp, fp+k);
  return k;
}


/*FA****************************************************************/
/*                                                                 */
/*  LSC::print                                                     */
/*                                                                 */
/*FE****************************************************************/

void LSC::print( ostream &s, int nw ) const

{
  FP *sc = new FP[noc];
  for( int c=0; c<noc; c++ ) {
    sc[c].number = c;
    sc[c].prob = cluster_prob[c];
  }
  sort(sc, sc+noc);

  s << "\nNumber of Clusters " << noc << "\n";
  s << "Number of Features " << nof << "\n";
  for( int i=0; i<noc; i++) {
    FNo c = sc[i].number;
    s << "------------------------\n";
    s << "Cluster " << c << "\t" << cluster_prob[c] << "\n";
    for( int f=0; f<nof; f++) {
      FP *fp = new FP[feature[f].size()];
      long n=sort_probs(fp, feature[f].size(), feature_prob[c][f] );
      s << "Feature " << f << "\n";
      for( long l=0; l<n && (nw==0 || l<nw); l++)
	s <<"\t"<< feature[f].name(fp[l].number) <<"\t"<< fp[l].prob <<"\n";
      delete[] fp;
    }
  }
  s << "\n";
  delete[] sc;
}


/*FA****************************************************************/
/*                                                                 */
/*  operator<<                                                     */
/*                                                                 */
/*FE****************************************************************/

ostream &operator<<( ostream &s, LSC &model )

{
  model.print(s);
  return s;
}


/*FA****************************************************************/
/*                                                                 */
/*  LSC:store_features                                             */
/*                                                                 */
/*FE****************************************************************/

void LSC::store_features( FILE *file ) const

{
  fwrite(&noc, sizeof(noc), 1, file);
  fwrite(&nof, sizeof(nof), 1, file);

  // store the feature names
  for( int f=0; f<nof; f++) {
    FNo n=feature[f].size();
    fwrite(&n, sizeof(n), 1, file);
    for( long w=0; w<n; w++ ) {
      char *s=feature[f].name(w);
      fwrite(s, sizeof(s[0]), strlen(s)+1, file);
    }
  }

  // store the cluster probabilities
  fwrite(cluster_prob, sizeof(cluster_prob[0]), noc, file);
}


/*FA****************************************************************/
/*                                                                 */
/*  LSC:store                                                      */
/*                                                                 */
/*FE****************************************************************/

void LSC::store( FILE *file ) const

{
  store_features( file );

  // store the feature probabilities for each cluster
  for( int c=0; c<noc; c++)
    for( int f=0; f<nof; f++)
      fwrite(feature_prob[c][f], sizeof(feature_prob[0][0][0]), 
	     feature[f].size(), file);
}


/*FA****************************************************************/
/*                                                                 */
/*  read_string                                                    */
/*                                                                 */
/*FE****************************************************************/

char *read_string( FILE *file )

{
  static char buffer[BUFFER_SIZE];
  for( int i=0; i<BUFFER_SIZE; i++) {
    int c=fgetc(file);
    if (c == EOF)
      throw "in binary LSC file!";
    buffer[i] = (char)c;
    if (c == 0)
      return buffer;
  }
  throw "in binary LSC file!";
}


/*FA****************************************************************/
/*                                                                 */
/*  LSC:read                                                       */
/*                                                                 */
/*FE****************************************************************/

void LSC::read( FILE *file )

{
  fread(&noc, sizeof(noc), 1, file);
  fread(&nof, sizeof(nof), 1, file);

  feature = new Feature[nof];
  cluster_prob = new float[noc];
  feature_prob = new float**[noc];

  // read the feature names
  for( int f=0; f<nof; f++) {
    FNo n;
    fread(&n, sizeof(n), 1, file);
    for( long w=0; w<n; w++ )
      feature[f].insert(read_string(file));
  }

  // read the cluster probabilities
  cluster_prob = new float[noc];
  fread(cluster_prob, sizeof(cluster_prob[0]), noc, file);

  // read the feature probabilities for each cluster
  feature_prob = new float**[noc];
  for( int c=0; c<noc; c++) {
    feature_prob[c] = new float*[nof];
    for( int f=0; f<nof; f++) {
      feature_prob[c][f] = new float[feature[f].size()];
      fread(feature_prob[c][f], sizeof(feature_prob[0][0][0]), 
	     feature[f].size(), file);
    }
  }
}


/*FA****************************************************************/
/*                                                                 */
/*  LSC:prob                                                       */
/*                                                                 */
/*FE****************************************************************/

double LSC::prob( const FNo *wn ) const

{
  double sum=0.0;
  for( int c=0; c<noc; c++) {
    double p=cluster_prob[c];
    for( int f=0; f<nof; f++) {
      if (wn[f] == -1)
	return 0.0;
      p *= feature_prob[c][f][wn[f]];
    }
    sum += p;
  }
  return sum;
}


/*FA****************************************************************/
/*                                                                 */
/*  LSC:prob                                                       */
/*                                                                 */
/*FE****************************************************************/

double LSC::prob( const char **w ) const

{
  FNo *wn = new FNo[nof];

  for( int f=0; f<nof; f++)
    wn[f] = feature[f].index(w[f]);
  double p=prob(wn);

  delete[] wn;
  return p;
}


/*FA****************************************************************/
/*                                                                 */
/*  LSC:prob                                                       */
/*                                                                 */
/*FE****************************************************************/

double LSC::prob( const char *w1, const char *w2 ) const

{
  FNo wn[2];

  wn[0] = feature[0].index(w1);
  wn[1] = feature[1].index(w2);

  return prob(wn);
}



/*FA****************************************************************/
/*                                                                 */
/*  LSC:perplexity                                                 */
/*                                                                 */
/*FE****************************************************************/

double LSC::perplexity() const

{
  double fsum=0.0;
  double psum=0.0;
  for( long d=0; d<data_size; d++) {
    psum += data[d].freq * log(prob(data[d].feature));
    fsum += data[d].freq;
  }
  return exp(-psum/fsum);
}


/*FA****************************************************************/
/*                                                                 */
/*  LSC:store_compact                                              */
/*                                                                 */
/*FE****************************************************************/

void LSC::store_compact( FILE *file, double threshold ) const

{
  store_features( file );
  
  // store the feature probabilities for each cluster
  for( int c=0; c<noc; c++)
    for( int f=0; f<nof; f++) {
      FP *fp = new FP[feature[f].size()];
      FNo i,n=sort_probs( fp, feature[f].size(), feature_prob[c][f] );
      double sum=0.0;
      for( i=0; i<n; i++)
	if (sum > threshold)
	  break;
	else
	  sum += fp[i].prob;
      for( n=0; n<i; n++)
	fp[n].prob = (float)(fp[n].prob / sum);
      fwrite(&n, sizeof(n), 1, file);
      fwrite(fp, sizeof(fp[0]), n, file);
      delete[] fp;
    }
}
