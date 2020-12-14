#include "util.h"

/*
    okay, I concede the parsing battle this time, back to python
*/

/*
    <bag> contain (<number> <bag> ,?)|(no other bags)*
*/

// Alright, since this is a pretty explicit graph problem
// I will use an Adjacency Matrix with an array
// to map the indices [0, n] to the different bag names.
// toy example shown below would represent a graph
// where a yellow bag can contain 2 blue bags
/*              <yellow bag>    <blue bag>
    <yellow bag>     0              2
    <blue bag>       0              0

*/
struct BagMatrix {
    struct Array* key;
    int **containment_matrix;
    int num_bags;
};

void free_matrix(struct BagMatrix* m){
    // free other stuff in m
    for (int i=0; i < m->num_bags; i++){
        free(m->containment_matrix[i]);
    }
    free(m->containment_matrix);
    // since this is not a Cello struct we manually deallocate the array
    del_root(m->key);
    free(m);
    return;
}

/*I should probably add this to util.h l8r*/
struct Array* parse_lookahead(struct String* str, char* delimiter, int size){
    
    struct String* before_delimiter = new(String);
    struct String* after_delimiter = new(String);
   
    struct Array* strArr = new(Array, String);
  
    int pos = 0;

    char temp_str[2] = {' ', '\0'};
    struct String* temp = new(String);

    bool delim_found = false;

    // while the delimiter could still be in the buffer
    while ( pos < len(str)-size+1 ){

        for (int i=pos; i < pos+size; i++){
            temp_str[0] = str->val[i];
            append(temp, $S(temp_str));
        }
        // check if we found the delimiter
        if (strcmp(temp->val, delimiter) == 0) {
            // set flag mentioning that we found the delimiter
            delim_found = true;

            // read the rest of string into after_delimiter
            for (int i=pos+size; i < len(str); i++){
                temp_str[0] = str->val[i];
                append(after_delimiter, $S(temp_str));
            }
            // return before delimiter
            break;
        };

        //otherwise we read the content into the before_delimiter
        temp_str[0] = str->val[pos];
        append(before_delimiter, $S(temp_str)); 
        pos++;

        // reset temp string
        resize(temp, 0);
        
    }
    
    if (delim_found == false) return NULL;

    push(strArr, before_delimiter);
    push(strArr, after_delimiter);
    

    return strArr;
}

int find_key(struct BagMatrix* mat, struct String* keyStr){
    int keyIndex = -1;
    println("finding key for %$", keyStr);
    for (int i=0; i < len(mat->key); i++){
        if (strcmp(keyStr->val, ((struct String*)get(mat->key, $I(i)))->val) == 0){
            keyIndex = i;
            break;
        }
    }
    return keyIndex;
}

// add unique bag key string to matrix
// ignore redundent calls
void add_bag_key(struct BagMatrix* matrix, struct String* key){
    int index = find_key(matrix, key);
    if (index == -1){
        push(matrix->key, key);
    }
}

void add_rule(struct BagMatrix* matrix, struct String* container, struct String* containee, int weight){
    add_bag_key(matrix, containee); add_bag_key(matrix, container);
    matrix->containment_matrix[find_key(matrix, container)][find_key(matrix, containee)] = weight;
    return;
}

/*This is where the pain begins*/
struct BagMatrix* read_matrix_from_text(struct String* text){
    struct Array* rules = split_string_by_character(text, "\n");
    struct BagMatrix* new_mat = malloc(sizeof(struct BagMatrix));
    

    new_mat->key = new_root(Array, String);

    new_mat->num_bags = len(rules); 
    new_mat->containment_matrix = malloc(sizeof(bool*) * new_mat->num_bags);
    for (int i=0; i < new_mat->num_bags; i++){
        new_mat->containment_matrix[i] = calloc(new_mat->num_bags, sizeof(bool));
    }

    /*Now we read each rule (I want death)*/
    for (int i=0; i< new_mat->num_bags; i++){
        // parse bagname
        struct Array* step_arr = parse_lookahead(get(rules, $I(i)), " contain ", strlen(" contain "));
        struct String* bag_name = get(step_arr, $I(0));
        // parse inner bags
        struct String* contained = get(step_arr, $I(1));

        /*Parse each rule*/
        step_arr = parse_lookahead(contained, ", ", strlen(", "));
        int next_weight = 0;
        char* temp_str;

        while (step_arr != NULL){
            // parsed rule should be in form "%d %s %s %s"
            struct String* parsed_rule = get(step_arr, $I(0));
            // read the numeric quantity
            struct Array* number_and_name = parse_lookahead(parsed_rule, " ", strlen(" "));
            struct String* number = get(number_and_name, $I(0));
            struct String* containee_name = get(number_and_name, $I(1));
            next_weight = atoi(number->val); 
            // read the rest of the bag name into a string
            add_rule(new_mat, bag_name, containee_name, next_weight);
            contained = get(step_arr, $I(1));
            step_arr = parse_lookahead(contained, ", ", strlen(", "));
        }

        // parse final rule
        step_arr = parse_lookahead(contained, ".", strlen("."));
        struct String* final_rule = get(step_arr, $I(0));
        struct Array* number_and_name = parse_lookahead(contained, " ", strlen(" "));
        next_weight = atoi(((struct String*) get(number_and_name, $I(0)))->val);
        add_rule(new_mat, bag_name, get(number_and_name, $I(1)), next_weight);

    }

    return new_mat;
}


void test(struct String* s, char* delim){
    struct Array* test_arr = parse_lookahead(s, delim, strlen(delim));
    printf("Testing string \"%s\" with delimiter \"%s\":\n", s->val, delim);
    if (test_arr == NULL){
        println("Delimiter not found.");
    } else {
        printf("Before delimiter: \"%s\", after delimiter: \"%s\".\n", ((struct String*)get(test_arr, $I(0)))->val, ((struct String*)get(test_arr, $I(1)))->val);
    }

}

int main(int argc, char **argv){
    FILE* fptr = validate_args(argc, argv);
    struct BagMatrix* bag_graph = read_matrix_from_text(read_file_into_string(fptr));

    /*
    test($S("finding everything working well"), "everything");
    test($S("Woot, Woot, Woot!"), ",");
    test($S("This is my big break.... YAY"), "walrus");
    test($S("this is my final attempt."), ".");
    */

    fclose(fptr);
    free_matrix(bag_graph);
    return 0;
}