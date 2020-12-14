# Advent of Code 2020
My solutions (or attempts at solutions) for the 2020 Advent of Code.

## Tech-Stack
For this year I implemented my first 5 or so solutions in C with heavy usage of [Cello](http://libcello.org/home), a C Library which adds support for some nice high-level features.

However, after day 7-ish I got tired of parsing things and switched over to python 3 with all the same goodies

## Loading my solutions (WIP)
First, you'll need a c compiler & make as well as the Cello library installed system-wide for the solutions which use Cello.
For the solutions which use Python, you'll need python and whatever dependencies specified in the requirements.txt

After that you should be able to simply run: ```make day<number> input="filename"``` and the program should compile itself and then run with the supplied input file.

For example: ```make day1 input="./day1/input.txt"``` will compile my solution for day 1 and then run it with the supplied input file.

DISCLAIMER: I was developing my solutions on my personal windows laptop so if you're trying to load this solutions on a linux or MacOS system you'll probably have to tool around with my makefile a little bit (e.g. use ```rm -f``` instead of ```del /f```).






