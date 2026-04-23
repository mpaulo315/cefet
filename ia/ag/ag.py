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
                tx_mutacao: float,
                type: Literal["max", "min"], 
                funcao_roleta: Callable[[list[AbsIndividuo], int], list[AbsIndividuo]],
                plato_increase: float = 0.1,
                plato_size: int | None = None):
        self.factory = factory
        self.n = n
        self.elite = elite
        self.type = type
        self.tx_mutacao = tx_mutacao
        self.funcao_roleta = funcao_roleta
        self.plato_size = plato_size
        self.plato_increase = plato_increase

    def _aplicar_roleta(self, populacao: list[AbsIndividuo], qtd: int) -> list[AbsIndividuo]:
        return self.funcao_roleta(populacao, qtd)

    def executar(self, geracoes: int = 100) -> AbsIndividuo:
        populacao = [self.factory.criar_individuo() for _ in range(self.n)]
        hist_acumulado = []

        plato_trigger = 0
        plato_counter = 0

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
        dashboard.layout.width = "100%"

        fig.update_layout(autosize=True)

        
        fig.add_trace(go.Scatter(name="Melhor", x=[], y=[], mode="lines"), row=1, col=1)
        fig.add_trace(go.Scatter(name="Média", x=[], y=[], mode="lines"), row=1, col=1)
        fig.add_trace(go.Scatter(name="Pior", x=[], y=[], mode="lines"), row=1, col=1)
        fig.add_trace(go.Scatter(name="Desvio Padrão", x=[], y=[], mode="lines"), row=1, col=1)

        fig.add_trace(go.Histogram(name="Fitness", x=[], nbinsx=20), row=1, col=2)

        display(dashboard)

        df = pd.DataFrame(columns=["Geração", "Melhor", "Fitness (M)", "Pior", "Fitness (P)"])

        best = None
        is_plato = False
        for gen in range(geracoes):
            try:
                mutantes = [ind.mutar(self.tx_mutacao + self.plato_increase if is_plato else self.tx_mutacao) 
                            for ind in populacao]
                
                if is_plato and plato_trigger > 0:
                    plato_trigger -= 1
                    fig.update_shapes(
                        patch={
                            "x1": gen,
                        },
                        selector={
                            "name": f"plato_{plato_counter}"
                        }
                    )

                    if plato_trigger == 0:
                        is_plato = False

                filhos = []
                for i in range(0, self.n, 2):
                    if i + 1 < self.n:
                        try:
                            filhos.extend(populacao[i].recombinar(populacao[i + 1]))
                        except IndexError as e:
                            print(f"Erro ao recombinar indivíduos ({i}, {i + 1}): {e}")
                            print(f"Tam. população: {len(populacao)}")
                            print(f"N: {self.n}")
                            raise e

                nova_populacao = populacao + mutantes + filhos
                nova_populacao.sort(key=lambda ind: ind.fitness(), reverse=self.type == "max")

                populacao_elite = nova_populacao[:self.elite]
                sorteados = self._aplicar_roleta(nova_populacao[self.elite:], self.n - self.elite)
                
                populacao = populacao_elite + sorteados
                populacao.sort(key=lambda ind: ind.fitness(), reverse=self.type == "max")

                if self.plato_size is not None and \
                    not is_plato and \
                    best is not None and populacao[0].fitness() == best.fitness():
                    plato_trigger += 1

                    if plato_trigger == self.plato_size:
                        is_plato = True
                        plato_counter += 1
                        fig.add_vrect(
                            x0 = gen,
                            x1 = gen,
                            fillcolor = "red",
                            opacity = 0.3,
                            layer = "below",
                            line_width = 0,
                            name=f"plato_{plato_counter}",
                            row=1, col=1
                        )


                # Atualização do dashboard
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
            except Exception as e:
                print(f"Erro na geração {gen}: {e}")
                raise e


        return populacao[0]