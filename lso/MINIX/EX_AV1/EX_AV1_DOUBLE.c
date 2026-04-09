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

    pid_t filho1, filho2;
    int status;
    int middle = 500000;
    
    struct timeval start, end;
    filho1 = fork();

    if (filho1 == 0) {
        gettimeofday(&start, NULL);

        for (int i = 0; i < middle; i++) {
            if (data[i] == search_value) {
                printf("Valor %d encontrado no index %d pelo child 1\n", search_value, i);
                break;
            }
        }
        
        gettimeofday(&end, NULL);
        
        long micro = (end.tv_sec - start.tv_sec) * 1000000 + end.tv_usec - start.tv_usec;
        printf("Child 1 | Tempo de execução: %ld us\n", micro);  

        exit(0);
    }

    filho2 = fork();

    if (filho2 == 0) {
        gettimeofday(&start, NULL);

        for (int i = middle; i < ARRAY_SIZE; i++) {
            if (data[i] == search_value) {
                printf("Valor %d encontrado no index %d pelo child 2\n", search_value, i);
                break;
            }
        }

        gettimeofday(&end, NULL);
        long micro = (end.tv_sec - start.tv_sec) * 1000000 + end.tv_usec - start.tv_usec;
        printf("Child 2 | Tempo de execução: %ld us\n", micro);

        exit(0);
    }

    wait(&status);
    wait(&status);

    return 0;

}