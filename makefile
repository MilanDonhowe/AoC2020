CC=gcc
CFLAGS=-g -lcello -lDbgHelp
VPATH=$(wildcard day*)

day3: solution_day_3
	$< $(input)

solution_day_3: solution_day_3.c
	$(CC) $^ -o solution_day_3 $(CFLAGS)

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
