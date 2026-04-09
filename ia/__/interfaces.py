from abc import ABC, abstractmethod

class Individuo(ABC):
    _genes: list[int]

    @abstractmethod
    def recombinar(self, outro: "Individuo") -> list["Individuo"]:
        pass

    @abstractmethod
    def mutar(self, taxa_mutacao: float = 0.1) -> "Individuo":
        pass

    @abstractmethod
    def avaliar(self) -> float:
        pass


class Factory(ABC):
    @abstractmethod
    def criar_individuo(self) -> Individuo:
        pass