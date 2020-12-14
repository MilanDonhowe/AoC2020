#include <Cello.h>

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

struct String* read_file_into_string(FILE* text_file){
    struct String* s = new(String);
    while (!feof(text_file)){
        char new_char[2] = {' ', '\0'};
        new_char[0] = (char) fgetc(text_file);
        append(s, $S(new_char));
    }
    return s;
}


struct Array* get_groups(struct String* str){
    struct Array* groups = new(Array, String);
    uint8_t new_lines = 0;
    char temp_str[2] = {' ', '\0'};
    struct String* next_string = new(String);
    for (int i=0; i < len(str); i++){
        new_lines = (str->val[i] == '\n') ? new_lines+1 : 0; 
        if (new_lines == 2){
            new_lines = 0;
            push(groups, next_string);
            resize(next_string, 0);
        }
        temp_str[0] = str->val[i];
        append(next_string, $S(temp_str));
    }
    // add last group
    if (len(next_string)){
        push(groups, next_string);
    };
    return groups;
}

// gets union
int count_unique_answers(struct String* str){
    const int size = 256;
    int instances[256];
    for (int i=0; i<size;i++) instances[i] = 0;

    for (int i=0; i < len(str); i++){
        instances[str->val[i]] = 1;
    }
    instances['\n'] = 0;
    int count = 0;
    for (int i=0; i < size; i++){
        if (instances[i]) count++;
    }

    return count;
}

/*Basically counts the union of all answers in a group*/
int part_one_count(struct Array* strArr){
    int total_sum = 0;
    for (int i=0; i < len(strArr); i++){
        total_sum += count_unique_answers(get(strArr, $I(i)));
    }
    return total_sum;
}

struct Array* split_group(struct String* str){
    // strtok magic
    struct Array* strArr = new(Array, String);
    char* ptr = strtok(str->val, "\n");
    while (ptr){
        // need to make sure I'm not treating blank lines as answers....
        if (isalpha(ptr[0])) push(strArr, $S(ptr));
        ptr = strtok(NULL, "\n");
    }
    /* 
    foreach (s in strArr){
        struct String *str = s;
        println("%$ %i", s, $I(isalpha(str->val[0])));
    }
    */
    
    return strArr;
}

int intersection(struct Array* strArr){
    int group_sum = 0;

    int qualification = len(strArr);

    // similar process as getting the union but we increment each answer location
    // if an answer is present in all the answer sets then that index will store an integer
    // equal to the number of answer sets
    
    // had to do manual zeroing of memory
    // would have used the heap but Cello got mad for some reason
    int instances[256];
    for (int i=0; i < 256; i++) instances[i] = 0;

    for (int i=0; i < qualification; i++){
        struct String* str = get(strArr, $I(i));
        for (int j=0; j < len(str); j++){
            instances[str->val[j]]++;
        }
    }
    instances['\n'] = 0;
    for (int i=0; i < 256; i++){
        if (instances[i] == qualification) group_sum++;
    }


    return group_sum;
}

// counts the intersection of each group set
int part_two_count(struct Array* strArr){
    int total_sum = 0;
    struct String* this_group;
    for (int i=0; i < len(strArr); i++){
        this_group = get(strArr, $I(i));
        struct Array* answers = split_group(this_group);
        total_sum += intersection(answers);
    }
    return total_sum;
}

int main(int argc, char **argv){
    FILE* fptr = validate_args(argc, argv);

    struct Array* groups = get_groups(read_file_into_string(fptr));
    /*
    foreach(g in groups){
        println("%$", g);
    }
    */
    printf("sum for part 1 is %i\n", part_one_count(groups));
    printf("sum for part 2 is %i\n", part_two_count(groups));

    fclose(fptr);
    return 0;
}