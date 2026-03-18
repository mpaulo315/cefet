from enum import Enum
from typing import Literal
from itertools import combinations
from colorama import Fore, Style, init

import sympy as sp
from numpy import inf, isinf
from sympy.plotting import plot_implicit

import json
from pathlib import Path

folder = Path(__file__).parent
init(autoreset=True)

class Restricao:
    def __init__(self, 
                coeficientes: list[float], 
                sinal: Literal["<=", ">=", "==", "!=", "<", ">"],
                rhs: float):
        self.coeficientes = coeficientes
        self.sinal = sinal
        self.rhs = rhs

class PPLObjetivo(str, Enum):
    MAX = "MAX"
    MIN = "MIN"

class PPLGrafico:
    def __init__(self, 
                objetivo: PPLObjetivo,
                coeficientes: list[float],
                restricoes: list[Restricao]):
        self.objetivo = objetivo
        self.coef_objetivo = coeficientes
        self.variaveis = []

        for i in range(len(coeficientes)):
            self.variaveis.append(sp.Symbol(f"x{i}"))

        self.expr_objetivo = sum(coef * self.variaveis[i] for i, coef in enumerate(coeficientes))
        self.restricoes = restricoes.copy()
        
        for restricao in self.restricoes:
            restricao["expr"] = (
                sum(coef * self.variaveis[i] for i, coef in enumerate(restricao["coeficientes"])) - restricao["rhs"]
            )
        
        self.valor_final = -inf if self.objetivo == PPLObjetivo.MAX else inf
        self.solucao_final = None
        
    def calcular_intersecoes(self) -> list[float]:
        sistemas = list(combinations([x["expr"] for x in self.restricoes], len(self.variaveis)))
        solucoes = []
        for sistema in sistemas:
            solucoes.append(sp.solve(sistema, self.variaveis))

        return list(filter(lambda x: bool(x), solucoes))
    
    def satisfaz_restricoes(self, solucao: dict[sp.Symbol, float]) -> bool:
        # for var in self.variaveis:
        #     if var not in solucao:
        #         return False
            
        #     if not isinstance(solucao[var], float):
        #         return False

        for restricao in self.restricoes:
            resultado = restricao["expr"].subs(solucao)

            match restricao["sinal"]:
                case "<=":
                    if resultado > 0:
                        return False
                case ">=":
                    if resultado < 0:
                        return False
                case "==":
                    if resultado != 0:
                        return False
                case "!=":
                    if resultado == 0:
                        return False
                case "<":
                    if resultado >= 0:
                        return False
                case ">":
                    if resultado <= 0:
                        return False
        else:
            return True

    def aplicar_funcao_objetivo(self, solucao: dict[sp.Symbol, float]) -> float:
        return self.expr_objetivo.subs(solucao)
    

    def calcular_valor_final(self):
        if not isinf(self.valor_final):
            return 

        for solucao in self.calcular_intersecoes():
            if self.satisfaz_restricoes(solucao):
                valor = self.aplicar_funcao_objetivo(solucao)

                match self.objetivo:
                    case "MAX":
                        if valor > self.valor_final:
                            self.valor_final = valor
                            self.solucao_final = solucao

                    case "MIN":
                        if valor < self.valor_final:
                            self.valor_final = valor
                            self.solucao_final = solucao
    
    def processar(self):
        vertices = self.calcular_intersecoes()
        for v in vertices:
            if self.satisfaz_restricoes(v):
                valor = self.aplicar_funcao_objetivo(v)

                match self.objetivo:
                    case "MAX":
                        if valor > self.valor_final:
                            self.valor_final = valor
                            self.solucao_final = v
                    case "MIN":
                        if valor < self.valor_final:
                            self.valor_final = valor
                            self.solucao_final = v

    def print_resultado(self):
        print(f"{Fore.CYAN}Objetivo:{Style.RESET_ALL} {Style.BRIGHT}{self.objetivo}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Função objetivo:{Style.RESET_ALL} Z = {self.expr_objetivo}")
        
        print(f"\n{Fore.CYAN}Restrições:{Style.RESET_ALL}")
        for r in self.restricoes:
            expr_legivel = f"{r['expr'] + r['rhs']} {r['sinal']} {r['rhs']}"
            print(f"  {Fore.YELLOW}-{Style.RESET_ALL} {expr_legivel}")
        
        print()
        solucao_str = self.solucao_final
        resultado_str = f"Z = {self.valor_final}"
        
        print(
            f"{Fore.CYAN}Solução ótima:{Style.RESET_ALL} "
            f"{Fore.GREEN}{Style.BRIGHT}{solucao_str}{Style.RESET_ALL}"
            f"{'':>10}"
            f"{Fore.CYAN}Solução aplicada:{Style.RESET_ALL} "
            f"{Fore.GREEN}{Style.BRIGHT}{resultado_str}{Style.RESET_ALL}"
        )





    def __repr__(self):
        return (
            f"Objetivo: {self.objetivo}\n"
            f"Func. Objetivo: Z = {self.expr_objetivo}\n"
            f"Coeficientes: {self.coef_objetivo}\n"
            f"Variaveis: {self.variaveis}\n"
            f"Restricoes: {self.restricoes}\n"
        )
            
if __name__ == "__main__":
    with open(folder / "problems.json") as f:
        problems = json.load(f)

        for p in problems:
            ppl = PPLGrafico(**p)
            ppl.processar()
            ppl.print_resultado()
            print("="*50 + "\n")