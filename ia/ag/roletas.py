import numpy as np
from interfaces import AbsIndividuo

class Roleta:
    @classmethod
    def simples_maximo(cls, individuos: list[AbsIndividuo], qtd: int) -> list[AbsIndividuo]:
        selecionados = []

        total_fitness = sum(ind.fitness() for ind in individuos)
        probabilidades = [ind.fitness() / total_fitness for ind in individuos]

        while len(selecionados) < qtd and individuos:
            r = np.random.uniform(0, total_fitness)
            acumulado = 0
            for idx, (ind, prob) in enumerate(zip(individuos, probabilidades)):
                acumulado += prob * total_fitness
                if r < acumulado or len(individuos) == 1 and len(selecionados) < qtd:
                    selecionados.append(ind)
                    del individuos[idx]
                    break 

        if len(selecionados) < qtd:
            print(f"Indivíduos restantes: {len(individuos)}, Selecionados: {len(selecionados)}, Desejado: {qtd}")
            raise ValueError("Não foi possível selecionar a quantidade desejada de indivíduos.")

        return selecionados
    
    @classmethod
    def simples_minimo(cls, individuos: list[AbsIndividuo], qtd: int) -> list[AbsIndividuo]:
        selecionados = []
        
        total_fitness = sum(1 / (ind.fitness() + 1e-9) for ind in individuos)
        probabilidades = [(1 / (ind.fitness() + 1e-9)) / total_fitness for ind in individuos]

        while len(selecionados) < qtd and individuos:
            r = np.random.uniform(0, total_fitness)
            acumulado = 0
            for idx, (ind, prob) in enumerate(zip(individuos, probabilidades)):
                acumulado += prob * total_fitness
                if r < acumulado or len(individuos) == 1 and len(selecionados) < qtd:
                    selecionados.append(ind)
                    del individuos[idx]
                    break
        
        if len(selecionados) < qtd:
            print(f"Indivíduos restantes: {len(individuos)}, Selecionados: {len(selecionados)}, Desejado: {qtd}")
            raise ValueError("Não foi possível selecionar a quantidade desejada de indivíduos.")

        return selecionados
    
    @staticmethod
    def torneio_minimo(cls, individuos: list[AbsIndividuo], qtd: int) -> list[AbsIndividuo]:
        selecionados = []

        for _ in range(qtd):
            cand1, cand2 = np.random.choice(np.array(individuos), size=2, replace=False)
            selecionados.append(cand1 if cand1.fitness() < cand2.fitness() else cand2)
        return selecionados