import numpy as np
from interfaces import AbsFactory, AbsIndividuo
from typing import Self

class Rainha(AbsIndividuo):    
    def __init__(self, qtd_genes: int, empty: bool = False):
        super().__init__(qtd_genes)

        if empty:
            self._genes = np.zeros(qtd_genes)
        else:
            self._genes = np.random.permutation(qtd_genes)

    def recombinar(self, outro: AbsIndividuo) -> list[AbsIndividuo]:
        start, end = sorted(np.random.choice(len(self._genes), 2))
        filho1 = Rainha(len(self._genes), empty=True)
        filho2 = Rainha(len(self._genes), empty=True)

        dna1_p1 = np.take(self._genes, range(0, start), mode='wrap')
        dna1_p2 = np.take(outro._genes, range(start, end), mode='wrap')
        dna1_p3 = np.take(self._genes, range(end, len(self._genes)), mode='wrap')
        filho1._genes = np.concatenate([dna1_p1, dna1_p2, dna1_p3])

        dna2_p1 = np.take(outro._genes, range(0, start), mode='wrap')
        dna2_p2 = np.take(self._genes, range(start, end), mode='wrap')
        dna2_p3 = np.take(outro._genes, range(end, len(self._genes)), mode='wrap')
        filho2._genes = np.concatenate([dna2_p1, dna2_p2, dna2_p3])

        return [filho1, filho2]
    
    def mutar(self, tx_mutacao: float) -> AbsIndividuo:
        mutante = Rainha(len(self._genes), empty=True)
        mutante._genes = self._genes.copy()

        if np.random.rand() < tx_mutacao:
            if np.random.rand() >= 0.5:
                #Troca genes
                i, j = np.random.choice(len(mutante._genes), 2)
                mutante._genes[i], mutante._genes[j] = mutante._genes[j], mutante._genes[i]
            else:
                # Introduz novos genes
                pos = np.random.randint(0, len(self._genes) - 1)
                mutante._genes[pos] = np.random.randint(0, len(self._genes) - 1)

        return mutante

    def fitness(self) -> float:
        n = len(self._genes)
        idx = np.arange(n)
        diag = self._genes - idx
        anti_diag = self._genes + idx

        conflitos = len(self._genes) - len(np.unique(self._genes))  # Conflitos na mesma coluna
        conflitos += len(self._genes) - len(np.unique(diag))  # Conflitos na diagonal principal
        conflitos += len(self._genes) - len(np.unique(anti_diag))  # Conflitos na diagonal secundária

        return conflitos 

class FactoryRainhas(AbsFactory):
    def __init__(self, qtd_genes:    int, tx_mutacao: float):
        super().__init__(qtd_genes, tx_mutacao)

    def criar_individuo(self) -> Rainha:
        return Rainha(self.qtd_genes)