#include <Cello.h>

enum BLOCK_TYPE {
    EMPTY = 0,
    TREE
};

struct BlockRow {
    int size;
    enum BLOCK_TYPE *blocks;
};

bool tree_in_row(struct BlockRow* self, int pos){
    // simple modulo arithmetic since the pattern repeats
    return (self->blocks[pos % self->size] == TREE) ? true : false;
}

void BlockRow_Del(var self){
    struct BlockRow* br = self;
    if (br->blocks != NULL){
        free(br->blocks);
        br->blocks = NULL;
    }
    return;
}

void BlockRow_Assign(var self, var other){
    struct BlockRow* block_self = self;
    struct BlockRow* block_other = other;
    if (block_self->blocks != NULL){
        free(block_self->blocks);
        block_self->blocks = NULL;
    }
    block_self->size = block_other->size;
    block_self->blocks = calloc(block_self->size, sizeof(enum BLOCK_TYPE));
    for (int i=0; i<block_self->size; i++){
        block_self->blocks[i] = block_other->blocks[i]; 
    }
    return;
}

var BlockRow = Cello(BlockRow, Instance(New, NULL, BlockRow_Del), Instance(Assign, BlockRow_Assign));

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

struct Array* build_grid_from_file(FILE* grid_file){
    struct Array* grid_array = new(Array, BlockRow);
    int row_width = 0;
    while (fgetc(grid_file) != '\n') row_width++;
    // go back to the beginning of the file after getting the width
    fseek(grid_file, 0, SEEK_SET);

    while (!feof(grid_file)){
        struct BlockRow* next_row = $(BlockRow, row_width, calloc(row_width, sizeof(enum BLOCK_TYPE)));
        char* row_string = calloc(row_width, sizeof(char));
        fscanf(grid_file, "%s\n", row_string);
        for (int i=0; i < row_width; i++){
            if (row_string[i] == '#') next_row->blocks[i] = TREE;
        } 
        push(grid_array, next_row);
    }    


    return grid_array;
}

uint64_t count_trees(struct Array* grid, const int vertical_shift, const int horizontal_shift){
    uint64_t tree_count = 0;
    int right_pos = 0;
    // so we DO check the first position (this is unstated in the problem statement)
    // as such row = 0 and we apply the horizontal shift afterwards
    for(int row = 0; row < len(grid); row += vertical_shift){
        if (tree_in_row(get(grid, $I(row)), right_pos)) tree_count++;
        right_pos += horizontal_shift;
    }

    return tree_count;
}

int main(int argc, char **argv){
    struct Array* grid = build_grid_from_file(validate_args(argc, argv));
    println("There are %i trees for part 1", $I(count_trees(grid, 1, 3)));
    printf("All tree sums multipled together equal %lu for part 2\n", 
        count_trees(grid,1,5)*count_trees(grid,1, 1)*count_trees(grid, 1, 3)*count_trees(grid,1, 7)*count_trees(grid,2,1)
    );

    return 0;
}