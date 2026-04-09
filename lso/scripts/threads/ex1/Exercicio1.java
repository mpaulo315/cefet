package lso.scripts.threads.ex1;

import java.util.Scanner;

public class Exercicio1 extends Thread {
    public int id;

    public Exercicio1(int id) {
        this.id = id;
    }

    @Override
    public void run() {
        System.out.printf("Thread %d criada às %d ms%n", id, System.currentTimeMillis());
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Programa iniciado às " + System.currentTimeMillis() + " ms");
        System.out.println();

        String mainPrompt = "Deseja:\n" +
                "[0] Sair\n" +
                "[1] Criar uma nova thread\n" +
                "Digite sua escolha:";
                
        System.out.println(mainPrompt);

        int answer = scanner.nextInt();
        scanner.nextLine(); // Consume the newline character

        while (answer == 1) {
            System.out.println("Digite o ID da thread:");

            int id = scanner.nextInt();
            Exercicio1 thread = new Exercicio1(id);
            thread.start();

            System.out.println(mainPrompt);
            answer = scanner.nextInt();
            scanner.nextLine(); // Consume the newline character

        }
    }
}