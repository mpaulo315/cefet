from typing import Literal, Callable
from interfaces import AbsIndividuo, AbsFactory
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import ipywidgets as widgets
from IPython.display import display
import pandas as pd
import numpy as np

class AG:
    def __init__(self, 
                factory: AbsFactory, 
                n: int, 
                elite: int, 
                type: Literal["max", "min"], 
                funcao_roleta: Callable[[list[AbsIndividuo], int], list[AbsIndividuo]]):
        self.factory = factory
        self.n = n
        self.elite = elite
        self.type = type
        self.funcao_roleta = funcao_roleta

    def _aplicar_roleta(self, populacao: list[AbsIndividuo], qtd: int) -> list[AbsIndividuo]:
        return self.funcao_roleta(populacao, qtd)

    def executar(self, geracoes: int = 100) -> AbsIndividuo:
        populacao = [self.factory.criar_individuo() for _ in range(self.n)]
        hist_acumulado = []

        output_table = widgets.Output()

        fig = go.FigureWidget(
                make_subplots(
                    rows=1, 
                    cols=2,
                    subplot_titles=["Evolução", "Distribuição"],
                    specs=[[{"type": "xy"}, {"type": "histogram"}]],
                    column_widths=[0.4, 0.6]
                )
        )

        dashboard = widgets.VBox([fig, output_table])

        fig.update_layout(template="plotly_dark")

        fig.add_trace(go.Scatter(name="Melhor", x=[], y=[], mode="lines"), row=1, col=1)
        fig.add_trace(go.Scatter(name="Média", x=[], y=[], mode="lines"), row=1, col=1)
        fig.add_trace(go.Scatter(name="Pior", x=[], y=[], mode="lines"), row=1, col=1)
        fig.add_trace(go.Scatter(name="Desvio Padrão", x=[], y=[], mode="lines"), row=1, col=1)

        fig.add_trace(go.Histogram(name="Fitness", x=[], nbinsx=20), row=1, col=2)

        display(dashboard)

        df = pd.DataFrame(columns=["Geração", "Melhor", "Fitness (M)", "Pior", "Fitness (P)"])

        for gen in range(geracoes):
            mutantes = [ind.mutar() for ind in populacao]

            filhos = []
            for i in range(0, self.n, 2):
                if i + 1 < self.n:
                    filhos.extend(populacao[i].recombinar(populacao[i + 1]))

            nova_populacao = populacao + mutantes + filhos
            nova_populacao.sort(key=lambda ind: ind.fitness(), reverse=self.type == "max")


            populacao_elite = populacao[:self.elite]
            sorteados = self._aplicar_roleta(populacao[self.elite:], self.n - self.elite)
            
            populacao = populacao_elite + sorteados
            populacao.sort(key=lambda ind: ind.fitness(), reverse=self.type == "max")
            
            best = populacao[0]
            avg = sum(ind.fitness() for ind in populacao) / len(populacao)
            worst = populacao[-1]
            std = (sum((ind.fitness() - avg) ** 2 for ind in populacao) / len(populacao)) ** 0.5

            nova_linha = pd.DataFrame({
                "Geração": [gen],
                "Melhor": [best._genes],
                "Fitness (M)": [best.fitness()],
                "Pior": [worst._genes],
                "Fitness (P)": [worst.fitness()]
            })

            df = pd.concat([df, nova_linha], ignore_index=True)

            with fig.batch_update():
                fig.data[0].x += (gen,)
                fig.data[0].y += (best.fitness(),)

                fig.data[1].x += (gen,)
                fig.data[1].y += (avg,)

                fig.data[2].x += (gen,)
                fig.data[2].y += (worst.fitness(),)

                fig.data[3].x += (gen,)
                fig.data[3].y += (std,)

                hist_acumulado += [ind.fitness() for ind in populacao]
                fig.data[4].x = hist_acumulado
            
            with output_table:
                output_table.clear_output(wait=True)
                display(df.tail(10))


        return populacao[0]