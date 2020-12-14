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

struct Seat {
    int row;
    int col;
};

var Seat = Cello(Seat);

// read seat codes from file
struct Array* read_codes(FILE* fptr){
    struct Array* arr = new(Array, String);
    while(!feof(fptr)){
        struct String* new_code = new(String);
        resize(new_code, 11);
        fscanf(fptr, "%s\n", new_code->val);
        push(arr, new_code);
    }
    return arr;
}

void calc_code(struct String* pass, int* row, int* col){
    int row_tuple[2] = {0, 127};
    int col_tuple[2] = {0, 7};
    for (int i=0; i < len(pass); i++){
        int row_midpoint = row_tuple[0] + ((row_tuple[1] - row_tuple[0]) / 2);
        int col_midpoint = col_tuple[0] + ((col_tuple[1] - col_tuple[0]) / 2);
        switch (pass->val[i])
        {
        case 'F':
            row_tuple[1] = row_midpoint;
            break;
        case 'B':
            row_tuple[0] = row_midpoint + 1;
            break;
        case 'L':
            col_tuple[1] = col_midpoint;
            break;
        case 'R':
            col_tuple[0] = col_midpoint + 1;
            break;
        }
    }
    *row = row_tuple[0]; *col = col_tuple[1];
}

struct Array *count_codes(struct Array *strArr)
{
    struct Array *seatArr = new (Array, Seat);
    foreach (s in strArr)
    {
        struct Seat *nextSeat = new (Seat);
        struct String *str = s;
        calc_code(str, &(nextSeat->row), &(nextSeat->col));
        push(seatArr, nextSeat);
    }
    return seatArr;
}

int get_max_id(struct Array *seatArr)
{
    int max_id = 0;
    foreach (s in seatArr)
    {
        struct Seat *seat = s;
        int temp_id = (seat->row * 8) + seat->col;
        if (temp_id > max_id)
            max_id = temp_id;
    }

    return max_id;
}

struct Array* get_ids(struct Array* seatArr){
    struct Array* ids = new(Array, Int);
    foreach(s in seatArr){
        struct Seat *seat = s;
        int id = (seat->row * 8) + seat->col;
        push(ids, $I(id));
    }
    return ids;
}

int find_my_id(struct Array* idArr){
    for (int i=0; i < len(idArr); i++){
        int this_id = c_int(get(idArr, $I(i)));
        for (int j=0; j < len(idArr); j++){
            int next_id = c_int(get(idArr, $I(j)));
            if (this_id - next_id == 2){
                // now we check if the candidate exists in our list of boarding passes
                int candidate = (next_id + this_id)/2;
                for (int k=0; k < len(idArr); k++){
                    if (candidate == c_int(get(idArr, $I(k)))){
                        candidate = 0;
                        break;
                    }
                }
                if (candidate != 0) return candidate;
            }
        }
    }
    return 0;
}

int main(int argc, char **argv)
{
    FILE *seat_codes = validate_args(argc, argv);
    struct Array *codes = read_codes(seat_codes);
    struct Array *seats = count_codes(codes);

    /*Test cases:*/ 
    int row = 0; int col = 0;
    calc_code($S("BFFFBBFRRR"), &row, &col);
    printf("(%i, %i) should be (70, 7)\n", row, col); 
    calc_code($S("FBFBBFFRLR"), &row, &col);
    printf("(%i, %i) should be (44, 5)\n", row, col); 
    // part 1 & 2
    printf("the max seat ID is %d\n", get_max_id(seats));
    printf("my seat ID is %i\n", find_my_id(get_ids(seats)));
    fclose(seat_codes);
    return 0;
}