from abc import ABC, abstractmethod
from typing import Self
from numpy import ndarray

class AbsIndividuo(ABC):
    _genes: ndarray

    def __init__(self, qtd_genes: int):
        self._genes = ndarray(qtd_genes)

    @abstractmethod
    def recombinar(self, outro: Self) -> list[Self]:
        pass

    @abstractmethod
    def mutar(self, tx_mutacao: float) -> Self:
        pass

    @abstractmethod
    def fitness(self) -> float:
        pass


class AbsFactory(ABC):
    def __init__(self, qtd_genes: int, tx_mutacao: float):
        self.qtd_genes = qtd_genes
        self.tx_mutacao = tx_mutacao


    @abstractmethod
    def criar_individuo(self) -> AbsIndividuo:
        pass