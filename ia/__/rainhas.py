from random import randint

from ia.__.interfaces import Factory, Individuo


class IndRainhas(Individuo):
    _tx_mutacao = 0.3

    def __init__(self, qtd_genes: int):
        self._genes = [randint(0, qtd_genes - 1) for _ in range(qtd_genes)]

    def recombinar(self, outro: Individuo) -> list[Individuo]:
        ponto_corte = randint(1, len(self._genes) - 2)
        filho1 = IndRainhas(len(self._genes))
        filho2 = IndRainhas(len(self._genes))

        filho1._genes = self._genes[:ponto_corte] + outro._genes[ponto_corte:]
        filho2._genes = outro._genes[:ponto_corte] + self._genes[ponto_corte:]

        return [filho1, filho2]
    
    def mutar(self, taxa_mutacao: float = _tx_mutacao) -> "Individuo":
        if randint(0, 100) < taxa_mutacao * 100:
            pos = randint(0, len(self._genes) - 1)
            self._genes[pos] = randint(0, len(self._genes) - 1)

        return self

    def avaliar(self) -> float:
        pass

class FactoryRainhas(Factory):
    def criar_individuo(self) -> IndRainhas:
        return IndRainhas(8)