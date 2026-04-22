import numpy as np

from interfaces import AbsIndividuo

class Roleta:
    @classmethod
    def simples_maximo(cls, individuos: list[AbsIndividuo], qtd: int) -> list[AbsIndividuo]:
        selecionados = []

        for _ in range(qtd):
            total_fitness = sum(ind.fitness() for ind in individuos)
            probabilidades = [ind.fitness() / total_fitness for ind in individuos]

            for _ in range(qtd):
                r = np.random.uniform(0, total_fitness)
                acumulado = 0
                for ind, prob in zip(individuos, probabilidades):
                    acumulado += prob * total_fitness
                    if r < acumulado:
                        selecionados.append(ind)
                        del individuos[individuos.index(ind)]
                        break 

        
        return selecionados
    
    @classmethod
    def simples_minimo(cls, individuos: list[AbsIndividuo], qtd: int) -> list[AbsIndividuo]:
        selecionados = []
        
        for _ in range(qtd):
            total_fitness = sum(1 / (ind.fitness() + 1e-9) for ind in individuos)
            probabilidades = [(1 / (ind.fitness() + 1e-9)) / total_fitness for ind in individuos]

            for _ in range(qtd):
                r = np.random.uniform(0, total_fitness)
                acumulado = 0
                for ind, prob in zip(individuos, probabilidades):
                    acumulado += prob * total_fitness
                    if r < acumulado:
                        selecionados.append(ind)
                        del individuos[individuos.index(ind)]
                        break 

    @classmethod
    def minimo_com_seletor(cls, individuos: list[AbsIndividuo], qtd: int) -> list[AbsIndividuo]:
        selecionados = []

        for _ in range(qtd):
            total_fitness = sum(1 / (ind.fitness() + 1e-9) for ind in individuos)
            probabilidades = [(1 / (ind.fitness() + 1e-9)) / total_fitness for ind in individuos]

            for _ in range(qtd):
                r = np.random.uniform(0, total_fitness)
                acumulado = 0
                for ind, prob in zip(individuos, probabilidades):
                    acumulado += prob * total_fitness
                    if r < acumulado:
                        selecionados.append(ind)
                        del individuos[individuos.index(ind)]
                        break 


        
        return selecionados