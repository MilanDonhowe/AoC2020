CC=gcc
CFLAGS=-g -lcello -lDbgHelp
VPATH=$(wildcard day*)

day7: solution_day_7
	$< $(input)

solution_day_7: solution_day_7.c
	$(CC) $^ -o solution_day_7 $(CFLAGS)

day6: solution_day_6
	$< $(input)

solution_day_6: solution_day_6.c
	$(CC) $^ -o solution_day_6 $(CFLAGS)

day5: solution_day_5
	$< $(input)

solution_day_5: solution_day_5.c
	$(CC) $^ -o solution_day_5 $(CFLAGS)

day4: solution_day_4
	$< $(input)

solution_day_4: solution_day_4.c re.c
	$(CC) $^ -o solution_day_4 $(CFLAGS)

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
