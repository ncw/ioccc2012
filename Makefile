# Make file for Idwt project

CCPath		=
CCFlags		= -g -c -Wall -O2
# -g
#-pedantic -posix

Link		= $(CC)
LinkFlags	= -g -o $@
Libs		= -lm

binaries	= mersenne mersenne_crushed mersenne_final

all:		$(binaries)

mersenne_files = mersenne.o

mersenne:	$(mersenne_files)
		$(Link) $(LinkFlags) $(mersenne_files) $(Libs)

mersenne_crushed_files = mersenne_crushed.o

mersenne_crushed:	$(mersenne_crushed_files)
		$(Link) $(LinkFlags) $(mersenne_crushed_files) $(Libs)

mersenne_final_files = mersenne_final.o

mersenne_final:	$(mersenne_final_files)
		$(Link) $(LinkFlags) $(mersenne_final_files) $(Libs)

mersenne_crushed.c:	mersenne.c crush.py
		./crush.py mersenne.c mersenne_crushed.c
		./check.py mersenne_crushed.c
		grep -v '#include' mersenne_crushed.c > z.c
		gcc -E z.c > zz.c
		grep '#include' mersenne_crushed.c > out.c
		cat zz.c >> out.c 
		indent < out.c > mersenne_uncrushed.c
		rm z.c zz.c out.c

mersenne_final.c:	mersenne_crushed.c artify.py
		./artify.py mersenne_crushed.c mersenne.png > mersenne_final.c
		./check.py mersenne_final.c

clean:
		-rm -f *.o *.pyc $(binaries) core *~
		-rm -rf test

mrproper:	clean
		-rm -f mersenne_crushed.c mersenne_uncrushed.c mersenne_final.c

release:	clean
		zip -9 idwt-`date -I`.zip Makefile *.py *.txt *.c *.h *.s

test:		mersenne_final
		./unit_test.py mersenne_final

## Rule Patterns ##

.SUFFIXES:
.SUFFIXES:	.c .o

.c.o:;		$(CC) $(CCFlags) $< -o $@
