#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/time.h>

#define ARRAY_SIZE 1000000

int main() {
    int data[ARRAY_SIZE];
    for (int i = 0; i < ARRAY_SIZE; i++) {
        data[i] = i;
    }

    int search_value = -1;

    while (search_value < 0 || search_value >= ARRAY_SIZE) {
        printf("Escolha um valor (0-%d): ", ARRAY_SIZE - 1);
        scanf("%d", &search_value);
        printf("\n");
    }

    struct timeval start, end;
    gettimeofday(&start, NULL);
    for (int i = 0; i < 1000000; i++) {
        if (data[i] == search_value) {
            printf("Valor %d encontrado no index %d\n", search_value, i);
            break;
        }
    }
    gettimeofday(&end, NULL);
    long micro = (end.tv_sec - start.tv_sec) * 1000000 + end.tv_usec - start.tv_usec;
    printf("Tempo de execução single-threaded: %ld us\n", micro);

    
    return 0;

}