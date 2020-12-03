CC=gcc
CFLAGS=-O3 -lcello -lDbgHelp -g
VPATH=$(wildcard day*)

day2: solution_day_2
	$< $(input)

solution_day_2: solution_day_2.c
	$(CC) $^ -o solution_day_2 $(CFLAGS)

day1: solution_day_1
	$< $(input)

solution_day_1: solution_day_1.c
	$(CC)  $^ -o solution_day_1 $(CFLAGS)

clean:
	del /f *.exe
