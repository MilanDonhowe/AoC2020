/*
    Handy Utility Functions so I don't go insane re-writing parsing functions
    in C for every challenge.

*/
#ifndef UTIL_H
#define UTIL_H
#include <Cello.h>

/*
Function Name: validate_args
Parameters: # arguments, commandline arguments
Description: Accepts first passed argument as input text file and returns file pointer
             to the input text.
*/
FILE* validate_args(int count, char **args){
    if (count != 2){
        printf("Invalid number of arguments.  Proper usage: %s <input_file>", args[0]);
        exit(2);
    }
    FILE* file_test = fopen(args[1], "r");
    if (file_test == NULL){
        println("Couldn't open file named %s", $S(args[1]));
        exit(3);
    }
    return file_test;    
};


/*
Function Name: read_file_into_string
Parametesr: file pointer to text file
Description: Reads all text into a Cello string object.
*/
struct String* read_file_into_string(FILE* text_file){
    struct String* s = new(String);
    while (!feof(text_file)){
        char new_char[2] = {' ', '\0'};
        new_char[0] = (char) fgetc(text_file);
        append(s, $S(new_char));
    }
    return s;
};


struct Array* split_string_by_character(struct String* str, char* delim){
    // strtok magic
    struct Array* strArr = new(Array, String);
    char* ptr = strtok(str->val, delim);
    while (ptr){
        // need to make sure I'm not treating blank lines as answers....
        if (isalpha(ptr[0])) push(strArr, $S(ptr));
        ptr = strtok(NULL, delim);
    }
    return strArr; 
};


#endif