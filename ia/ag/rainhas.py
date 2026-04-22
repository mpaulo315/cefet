import numpy as np
from interfaces import AbsFactory, AbsIndividuo
from typing import Self


np.random.seed(42)
class Rainha(AbsIndividuo):    
    def __init__(self, qtd_genes: int, tx_mutacao: float = 0.1, empty: bool = False):
        super().__init__(qtd_genes, tx_mutacao)
        if empty:
            self._genes = np.zeros(qtd_genes)
        else:
            self._genes = np.random.randint(0, qtd_genes, size=qtd_genes)

    def recombinar(self, outro: AbsIndividuo) -> list[AbsIndividuo]:
        n = len(self._genes)
        ponto_corte = np.random.randint(1, len(self._genes) - 1)
        filho1 = Rainha(len(self._genes), self._tx_mutacao, empty=True)
        filho2 = Rainha(len(self._genes), self._tx_mutacao, empty=True)

        filho1._genes = self._genes[:(n - ponto_corte)] + outro._genes[ponto_corte:]
        filho2._genes = outro._genes[:(n - ponto_corte)] + self._genes[ponto_corte:]

        return [filho1, filho2]
    
    def mutar(self) -> AbsIndividuo:
        if np.random.randint(0, 100) < self._tx_mutacao * 100:
            pos = np.random.randint(0, len(self._genes) - 1)
            self._genes[pos] = np.random.randint(0, len(self._genes) - 1)

        return self

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
    def __init__(self, qtd_genes: int, tx_mutacao: float = 0.1):
        super().__init__(qtd_genes, tx_mutacao)

    def criar_individuo(self) -> Rainha:
        return Rainha(self.qtd_genes, self.tx_mutacao)