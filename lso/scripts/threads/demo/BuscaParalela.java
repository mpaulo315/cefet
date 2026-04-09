package lso.scripts.threads.demo;
import java.util.Scanner;

public class BuscaParalela {

    static final int TAMANHO = 1_000_000;
    static int[] vetor = new int[TAMANHO];

    // Resultado compartilhado entre as threads
    static volatile int indiceEncontrado = -1;

    static {
        for (int i = 0; i < TAMANHO; i++) {
            vetor[i] = i;
        }
    }

    // Thread de busca que estende a classe Thread
    static class ThreadBusca extends Thread {
        private final int inicio;
        private final int fim;
        private final int alvo;
        private final int id;

        public ThreadBusca(int id, int inicio, int fim, int alvo) {
            this.id = id;
            this.inicio = inicio;
            this.fim = fim;
            this.alvo = alvo;
        }

        @Override
        public void run() {
            System.out.printf("[Thread %d] Buscando no intervalo [%d, %d)...%n", id, inicio, fim);

            for (int i = inicio; i < fim; i++) {
                if (indiceEncontrado != -1) return;

                if (vetor[i] == alvo) {
                    indiceEncontrado = i;
                    System.out.printf("[Thread %d] Elemento %d encontrado no índice %d!%n", id, alvo, i);
                    return;
                }
            }

            System.out.printf("[Thread %d] Elemento não encontrado no intervalo [%d, %d).%n", id, inicio, fim);
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Digite o número inteiro a ser buscado (0 a 999999): ");
        int alvo = scanner.nextInt();
        scanner.close();

        int metade = TAMANHO / 2;

        ThreadBusca t1 = new ThreadBusca(1, 0, metade, alvo);
        ThreadBusca t2 = new ThreadBusca(2, metade, TAMANHO, alvo);

        long inicio = System.currentTimeMillis();

        t1.start();
        t2.start();

        t1.join();
        t2.join();

        long fim = System.currentTimeMillis();

        System.out.println();
        if (indiceEncontrado != -1) {
            System.out.printf("Resultado final: %d encontrado no índice %d.%n", alvo, indiceEncontrado);
        } else {
            System.out.printf("Resultado final: %d não encontrado no vetor.%n", alvo);
        }

        System.out.printf("Tempo de busca paralela: %d ms%n", fim - inicio);
    }
}