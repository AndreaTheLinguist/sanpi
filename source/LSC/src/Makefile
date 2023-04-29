
# TYPE is either debug, prof, static, debug2 or the empty string
TYPE = 

# uncomment the following line if hash_map is not found
SGILIB = -DSGIext

CXX = g++
WARNING = -Wall -Wcast-qual -Wcast-align -Wconversion -Wno-deprecated
ifeq ($(TYPE),debug)
  DEBUG = -ggdb
  OPTIMIZATION = -O0
else
  DEBUG = -DNDEBUG
  ifeq ($(TYPE),prof)
    OPTIMIZATION = -O2
    PROFILE = -pg
  else
    OPTIMIZATION = -O4
    ifeq ($(TYPE),debug2)
      DEBUG = -DDEBUG
    else
      ifeq ($(TYPE),static)
        STATIC = -static
      endif
    endif
  endif
endif

CFLAGS = $(DEBUG) $(PROFILE) $(OPTIMIZATION) $(WARNING) $(SGILIB)
LDFLAGS = $(DEBUG) $(PROFILE) $(STATIC)
CXXFLAGS = $(CFLAGS)

PROGRAM = lsc-train lsc-disambiguate lsc-perplexity lsc-print

OBJ = lsc.o


.PHONY: all clean realclean archive remake

all: $(PROGRAM)

%: $(OBJ) %.o
	$(CXX) -o $@ $^ $(LDFLAGS)

remake: clean $(PROGRAM)

clean:
	-rm y.tab.h y.output scanner.c fst-compiler.c *.o *~ Makefile.bak 2>&- > /dev/null

realclean: clean
	-rm $(PROGRAM) 2>&- > /dev/null

archive: clean
	gtar -zcf LSC-`date '+%y%m%d'`.tar.gz *.[Chyl] Makefile


# DO NOT DELETE

lsc-disambiguate.o: lsc.h
lsc-perplexity.o: lsc.h
lsc-print.o: lsc.h
lsc-train.o: lsc.h
lsc.o: lsc.h
