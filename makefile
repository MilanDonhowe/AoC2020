CC=gcc
CFLAGS=-O3 -lcello -g
VPATH=$(wildcard day*)


day1: solution_day_1 $(input)
	solution_day_1 $(input)

solution_day_1: solution_day_1.c
	$(CC)  $^ -o solution_day_1 $(CFLAGS)

clean:
	del /f *.exe
