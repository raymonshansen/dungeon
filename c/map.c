#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv){
    int width = 16;
    int height = 4;
    int y, x;
    // Allocate memory for the map
    int **map = (int**)malloc(height * sizeof(int*));
    for(y = 0; y < height; y++){
        map[y] = (int*)malloc(width * sizeof(int));
    }
    // Populate
    for(y = 0; y < height; y++){
        for(x = 0; x < width; x++){
            map[y][x] = 1;
            printf("(%d, %d), ", x, y);
        }
        printf("\n");
    }
}