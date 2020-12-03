#include <Cello.h>
#define INVALID_ARGS(count) ((count) != 2)

// read numbers from text file into array
var read_numbers(char* filename){
    var numeric_array = new(Array, Int);
    with (f in new(File, $S(filename), $S("r"))){
        int pos = 0;
        var number = $I(0);
        // loop thru file, reading each number
        while (!seof(f)){
            pos = scan_from(f, pos, "%d\n", number);
            push(numeric_array, number);
        }
    }
    return numeric_array;
}

int64_t find_product_part_one(var NumberArray){
    var term_one, term_two;
    for (size_t i=0; i < len(NumberArray)-1; i++){
        term_one = get(NumberArray, $I(i));
        for (size_t j=i; j < len(NumberArray); j++){
            term_two = get(NumberArray, $I(j));
            if (c_int(term_one)+c_int(term_two) == 2020){
                return c_int(term_one) * c_int(term_two);
            }
        }
    }
}

int64_t find_product_part_two(var NumberArray){
    var term_one, term_two, term_three;
    for (size_t i=0; i < len(NumberArray); i++){
        term_one = get(NumberArray, $I(i));
        for (size_t j=i; j < len(NumberArray); j++){
            term_two = get(NumberArray, $I(j));
            for (size_t k=j; k < len(NumberArray); k++){
                term_three = get(NumberArray, $I(k));
                if (c_int(term_one)+c_int(term_two)+c_int(term_three) == 2020){
                    return c_int(term_one)*c_int(term_two)*c_int(term_three);
                }
            }
        }
    }
}


// usage: ./solution_day_1 input.txt
int main(int argc, char** argv){
    if (INVALID_ARGS(argc)){
        println("invalid arguments. valid usage: %$ <input_file>", $S(argv[0]));
        return 2;
    }

    var NumbersFromFile = read_numbers(argv[1]);

    /*
    foreach (number in NumbersFromFile){
        println("%$", number);
    }
    */

    println("product for part one is %d", $I(find_product_part_one(NumbersFromFile)));
    println("product for part two is %d", $I(find_product_part_two(NumbersFromFile)));

    return 0;
}