/*MA****************************************************************/
/*                                                                 */
/*  FILE     lsc.h                                                 */
/*  MODULE   lsc                                                   */
/*  PROGRAM  lsc                                                   */
/*  AUTHOR   Helmut Schmid, IMS, University of Stuttgart           */
/*                                                                 */
/*  PURPOSE  definition of the LSC classes                         */
/*                                                                 */
/*ME****************************************************************/

#ifndef _LSC_H_
#define _LSC_H_

#include <stdio.h>
#include <string.h>
#include <set>

#include <vector>
using std::vector;

#include <iostream>
using std::ostream;
using std::cerr;

#include <algorithm>
using std::sort;

#ifdef SGIext

#include <ext/hash_map>
#include <ext/hash_set>
using __gnu_cxx::hash_map;
using __gnu_cxx::hash_set;
using __gnu_cxx::hash;

#else

#include <hash_map>
#include <hash_set>
using std::hash_map;
using std::hash_set;
using std::hash;

#endif

typedef double Freq;
typedef long FNo;


/*****************  class Feature  *********************************/

class Feature {

  struct eqstr {
    bool operator()(const char* s1, const char* s2) const
    { return strcmp(s1, s2) == 0; }
  };
  typedef hash_map<const char*, long, hash<const char*>, eqstr> StringHash;
  typedef StringHash::iterator iterator;

 private:
  FNo current_index;
  StringHash sh;
  vector<char*> nt;

 public:
  Feature() { current_index = 0; };
  ~Feature() {
    for( FNo i=0; i<current_index; i++ ) {
      sh.erase(nt[i]);
      free(nt[i]);
    }
  }

  long size() { return current_index; };

  long index( const char *s ) { 
    iterator p=sh.find(s); 
    if (p == sh.end())
      return -1;
    else
      return p->second;
  }

  long insert( const char *s ) { 
    iterator p=sh.find(s); 
    if (p != sh.end())
      return p->second;
    char *ns = strdup(s);
    sh[ns] = current_index;
    nt.push_back(ns);
    return current_index++;
  }

  char *name( long n ) const { 
    if (n >= 0 && n < current_index)
      return nt[n];
    return NULL;
  }
};


/*****************  class Data  ************************************/

class Data {

 public:
  short cluster;
  Freq freq;
  FNo *feature; 

  Data() { feature = NULL; };
  Data( int n ) { feature = new FNo[n]; };
  ~Data() { delete[] feature; };

};


/*****************  class LSC  *************************************/

class LSC {

 private:
  int nof;
  int noc;
  int quiet;

  Feature *feature;

  float *cluster_prob;
  float ***feature_prob;

  Freq *cluster_freq;
  Freq ***feature_freq;

  long data_size;
  Data *data;


  void store_features( FILE *file ) const;

 public:
  LSC() { 
    quiet = nof = noc = 0; 
    data_size = 0; 
    feature = NULL;
    cluster_prob = NULL;
    feature_prob = NULL;
    cluster_freq = NULL;
    feature_freq = NULL;
    data = NULL;
  };
  LSC( FILE *file, int c=20 );
  ~LSC();
  void init( int seed=1 );
  void estimate_freqs();
  void estimate_probs();
  void train() { estimate_freqs(); estimate_probs(); };
  void train( int n ) { 
    for( int i=1; i<=n; i++) {
      if (!quiet)
	cerr << "iteration "<< i << "\t";
      train();
      if (!quiet)
	cerr << "perplexity: " << perplexity() << "\n";
    }
  };
  void store( FILE *file ) const;
  void store_compact( FILE *file, double threshold=0.999 ) const;
  void read( FILE *file );
  int number_of_clusters() const { return noc; };
  int number_of_features() const { return nof; };
  double prob( const FNo* ) const;
  double prob( const char** ) const;
  double prob( const char*, const char* ) const;
  double perplexity() const;
  void print( ostream &s, int n=0 ) const;

  friend ostream &operator<<( ostream&, LSC& );
};

ostream &operator<<( ostream&, LSC& );


/*****************  class FP  ***************************************/

class FP {
public:
  FNo   number;
  float prob;
  bool operator< ( const FP p ) const  { return prob > p.prob; }
};

#endif
