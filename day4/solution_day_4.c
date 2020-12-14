#include <Cello.h>
// using small regex library for c since I'm not gonna abuse scanf to solve part 2
// credit to kokke, src: https://github.com/kokke/tiny-regex-c
#include "re.h"
#define FIELDS 7


struct String* read_file_into_string(FILE* text_file){
    struct String* s = new(String);
    while (!feof(text_file)){
        char new_char[2] = {' ', '\0'};
        new_char[0] = (char) fgetc(text_file);
        append(s, $S(new_char));
    }
    return s;
}


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
}


struct Array* read_passports(FILE* ptr){
    struct String *s = read_file_into_string(ptr);

    struct Array* passports = new(Array, String);

    uint8_t newlines = 0;
    struct String* next_string = new(String);
    char temp_str[2] = {' ', '\0'};

    for (int i = 0; i < len(s); i++){

        // get next character
        temp_str[0] = s->val[i];

        // is it a newline?
        if (temp_str[0] == '\n'){
            newlines++;
        } else { 
            newlines = 0;
        }
        
        if (newlines >= 2){
            push(passports, next_string);
            newlines = 0;
            resize(next_string, 0);
        }

        append(next_string, $S(temp_str)); 
    }
    // get last passport
    if (len(next_string)) push(passports, next_string);
    /*
    char* token = strtok(s->val, "\n\n");
    while (token) {
        push(passports, $S(token));
        token = strtok(NULL, "\n\n");
    } 
    */
    fclose(ptr);
    return passports; 
}

struct Array* count_valid_passports_part_1(struct Array* strArr, char** fields, int size){
    struct Array* valid_passports = new(Array, String);
    foreach(passport in strArr){
        struct String* passport_str = passport;
        bool valid = true;
        for (int i=0; i < size; i++){
            if (!strstr(passport_str->val, fields[i])) {
                valid = false;
                break;
            }
        }
        if (valid == true){
            push(valid_passports, passport_str);
        }
    }
    return valid_passports; 
}

int count_valid_passports_part_2(struct Array* strArr){
    int valid_passports = 0;

    const char* eye_tests[7] = {"ecl:amb","ecl:blu","ecl:brn","ecl:gry","ecl:grn","ecl:hzl","ecl:oth"};

    foreach(p in strArr){
        struct String* passport = p;
        bool valid = true;
        int throw_ewey = 0;
        // birthday test         
        if (re_match("byr:[1920-2002]", passport->val, &throw_ewey) == -1) {
            valid = false;
        } else {
            //println("birthday test passed");
        }
        // issue year test
        if (re_match("iyr:[2010-2020]", passport->val, &throw_ewey) == -1){
            valid = false;
        } else {
            //println("iyr test passed");
        }
        // expiration year test
        if (re_match("eyr:[2020-2030]", passport->val, &throw_ewey) == -1){
            valid = false;
        } else {
            //println("eyr test passed");
        }
        
        // height test
        if (re_match("hgt:[0-9]+cm", passport->val, &throw_ewey) != -1){
            sscanf(passport->val, "hgt:%dcm", &throw_ewey);
            printf("%i is throw_ewey\n", throw_ewey);
            if (!(throw_ewey >= 150 && throw_ewey <= 193)) valid = false;
        } else if (re_match("hgt:[0-9]+in", passport->val, &throw_ewey) != -1){
            sscanf(passport->val, "hgt:%din", &throw_ewey);
            if (!(throw_ewey >= 59 && throw_ewey <= 79)) valid = false;
        } else {
            valid = false;
        }


        // hcl test
        if (re_match("hcl:#[a-f0-9]+", passport->val, &throw_ewey) != -1){
            valid = false; // quantifiers not supported would have used [a-f0-9]{6} instead
        } else {
            //println("HCL test passed");
        }
        // ecl tests
        bool eye_test = false;
        for (int i = 0; i < 7; i++) {
            if (re_match(eye_tests[i], passport->val, &throw_ewey) != -1) eye_test = true;
        }
        if (eye_test == false){
            valid = false;
        } else {
            //println("eye test passed");
        }
        //pid test
        if (re_match("pid:\\d\\d\\d\\d\\d\\d\\d\\d\\d", passport->val, &throw_ewey) == -1){
            valid = false;
        } 

        if (valid == true)
        {
            valid_passports++;
        }
    }

    return valid_passports;
}

int main(int argc, char **argv)
{

    char *required_fields[FIELDS] = {
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid"};

    struct Array* passports = count_valid_passports_part_1(read_passports(validate_args(argc, argv)), required_fields, FIELDS);
    println("%d valid passports for part 1", $I(len(passports)));
    println("%d valid passports for part 2", $I(count_valid_passports_part_2(passports)));

    return 0;
}