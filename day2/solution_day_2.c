#include <Cello.h>
#include <stdio.h>
#define INVALID_ARGS(count) ((count) != 2)

struct Password {
    int min;
    int max;
    char letter;
    char* content;
};

/*
    Copy constructor for password which I forgot to define resulting in the memory getting corrupted
*/
void Password_Assign(var self, var obj){
    struct Password* pwd_self = self;
    struct Password* pwd_other = obj;
    pwd_self->min = pwd_other->min;
    pwd_self->max = pwd_other->max;
    pwd_self->letter = pwd_other->letter;
    int length = strlen(pwd_other->content);
    if (pwd_self->content != NULL){
        free(pwd_self->content);
    }
    if (pwd_other->content != NULL){
        // when I use malloc instead I end up with corrupted memory....
        // I guess Cello is super sensitive about having memory zero initialized
        pwd_self->content = calloc(length+1, sizeof(char));
        strncpy(pwd_self->content, pwd_other->content, length);
    }
    return;
}

void Password_Del(var self){
    struct Password* pwd = self;
    if (pwd->content != NULL) free(pwd->content);
    return;
}

// register struct with Cello along with destructor & copy constructor
var Password = Cello(Password, Instance(New, NULL, Password_Del), Instance(Assign, Password_Assign));


/*Cursed input reading function which took a century to complete*/
struct Array* read_passwords(const char *filename){
    struct Array* passwords = new(Array, Password);

    FILE* password_file = fopen(filename, "r");
    while (!feof(password_file)){
            struct Password* pwd = $(Password, 0, 0, '\0', NULL);
            fscanf(password_file, "%d-%d %c: ", &(pwd->min), &(pwd->max), &(pwd->letter));
            // read variable length string until End of Line
            char next_byte[2] = {'[', '\0'};
            struct String* pwd_str = new(String);
            while (!feof(password_file)) {
                next_byte[0] = fgetc(password_file);
                if (next_byte[0] == '\n') break;
                append(pwd_str, $S(next_byte));
            } 
            pwd->content = c_str(pwd_str);
            push(passwords, pwd);
    }
    fclose(password_file);
    return passwords;
}

void print_password(struct Password* pwd){
    println("%s with %c %d-%d", $S(pwd->content), $I(pwd->letter), $I(pwd->min), $I(pwd->max));
}

int determine_valid_passwords_part_one(struct Array* passwordArray){
    int valid_passwords = 0;

    for (int i=0; i < len(passwordArray); i++){
        struct Password* pwd = get(passwordArray, $I(i));

        char target = pwd->letter;
        int instances = 0;
        for(int chr = 0; chr < len($S(pwd->content)); chr++){
            if (pwd->content[chr] == target) instances++;
        }

        if ( (instances >= pwd->min) && (instances <= pwd->max) ){
            valid_passwords++;
        }
    }

    return valid_passwords;
}


int determine_valid_passwords_part_two(struct Array* passwordArray){
    /*Todo*/
    int valid_passwords = 0;
    foreach(item in passwordArray){
        struct Password* pwd = item;
        int instances = 0;
        if (pwd->content[pwd->min-1] == pwd->letter) instances++;
        if (pwd->content[pwd->max-1] == pwd->letter) instances++;
        if (instances == 1) valid_passwords++;
    }
    return valid_passwords;
}

int main(int argc, char **argv){
    if (INVALID_ARGS(argc)){
        println("invalid arguments!  Correct usage: %s <input_file>", $S(argv[0]));
        return 2;
    }

    struct Array* arr = read_passwords(argv[1]);

    println("there are %d passwords", $I(len(arr)));
    
    println("%d valid passwords for part 1", $I(determine_valid_passwords_part_one(arr)));
    println("%d valid passwords for part 2", $I(determine_valid_passwords_part_two(arr)));
    

    return 0;
}