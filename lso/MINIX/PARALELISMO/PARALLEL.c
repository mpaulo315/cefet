#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t filho1, filho2;
    int status;
    int var = 10;
    filho1 = fork();

    // if (filho1 < 0) {
    //     perror("Erro ao criar o primeiro filho");
    //     exit(1);
    // }

    if (filho1 == 0) {
        printf("Sou o filho 1. PID = %d, Pai = %d e variavel %d\n", getpid(), getppid(),var);
        //while(1);
        exit(0);
    }

    var = 20;
    filho2 = fork();

    // if (filho2 < 0) {
    //     perror("Erro ao criar o segundo filho");
    //     exit(1);
    // }

    if (filho2 == 0) {
        printf("Sou o filho 2. PID = %d, Pai = %d e variavel %d\n", getpid(), getppid(),var);
        var = 30;
        //while(1);
        exit(0);
    }

    printf("Sou o processo pai. PID = %d\n", getpid());

    waitpid(filho1, &status, 0);
    waitpid(filho2, &status, 0);

    printf("Os dois filhos terminaram e as variavel vale %d\n",var);

    return 0;
}
