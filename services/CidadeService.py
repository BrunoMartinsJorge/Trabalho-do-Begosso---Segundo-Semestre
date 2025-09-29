import json
import os
from typing import List, Optional, Any

from exceptions.ObjectNotExistsException import ObjectNotExistsException
from exceptions.ObjectExistsException import ObjectExistsException
from models.ArvoresBinaria import ArvoreBinaria
from models.Cidades import Cidades


class CidadeService:
    def __init__(self):
        self.arvore_binaria: List[ArvoreBinaria] = []
        self.pasta_archives = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "archives"
        )
        os.makedirs(self.pasta_archives, exist_ok=True)
        self.path_cidades = os.path.join(self.pasta_archives, "cidades.txt")

    def __ler_arquivo(self) -> List[dict]:
        if not os.path.exists(self.path_cidades):
            return []
        try:
            with open(self.path_cidades, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def __salvar_arquivo(self, cidades: List[dict]) -> None:
        with open(self.path_cidades, "w", encoding="utf-8") as f:
            json.dump(cidades, f, indent=4, ensure_ascii=False)

    def __verificar_se_codigo_existe(
        self, cidades: List[dict], nova_cidade: Cidades
    ) -> None:
        if any(nova_cidade.codigo == int(c["codigo"]) for c in cidades):
            raise ObjectExistsException(
                f"Cidade com código {nova_cidade.codigo} já existe!"
            )

    def inserir_cidade(self, nova_cidade: Cidades) -> str:
        cidades = self.__ler_arquivo()
        self.__verificar_se_codigo_existe(cidades, nova_cidade)

        cidades.append(nova_cidade.to_dict())
        self.__salvar_arquivo(cidades)

        return "Cidade Cadastrada!"

    def buscar_todas_cidades(self) -> List[Cidades]:
        dados_json = self.__ler_arquivo()
        return [
            Cidades(
                codigo=int(d["codigo"]),
                descricao=d["descricao"],
                estado=d["estado"],
            )
            for d in dados_json
        ]

    def buscar_cidade(self, codigo: int) -> Cidades:
        cidades = self.__ler_arquivo()
        cidade_dict: Optional[dict] = next(
            (c for c in cidades if int(c["codigo"]) == codigo), None
        )

        if not cidade_dict:
            raise ObjectNotExistsException("Cidade não encontrada!")

        return Cidades(**cidade_dict)

    def excluir_cidade(self, codigo: int) -> None:
        indices, raiz = self.carregar_arvore_binaria()
        dados: List[Cidades] = self.buscar_todas_cidades()

        if not indices or not dados:
            return None

        def encontrar_minimo(index):
            while indices[index].esquerda != -1:
                index = indices[index].esquerda
            return index

        def remover(atual_index, codigo):
            if atual_index == -1:
                return -1
            no = indices[atual_index]
            if codigo < no.info:
                no.esquerda = remover(no.esquerda, codigo)
            elif codigo > no.info:
                no.direita = remover(no.direita, codigo)
            else:
                if no.esquerda == -1 and no.direita == -1:
                    return -1
                if no.esquerda == -1:
                    return no.direita
                if no.direita == -1:
                    return no.esquerda
                min_index = encontrar_minimo(no.direita)
                no.info = indices[min_index].info
                no.index = indices[min_index].index
                no.direita = remover(no.direita, indices[min_index].info)
            return atual_index

        nova_raiz = remover(raiz, codigo)

        # Atualiza os dados
        dados = [c for c in dados if c.codigo != codigo]
        dados_json = [c.to_dict() for c in dados]
        self.__salvar_arquivo(dados_json)

        return nova_raiz

    def leitura_exaustiva(self):
        dados = self.buscar_todas_cidades()
        indices = self.carregar_arvore_binaria()
        usados = set()
        dados_ordenados = []

        while len(usados) < len(dados):
            menor = None
            for registro in indices[0]:
                codigo = registro.info
                if codigo not in usados:
                    if menor is None or codigo < menor.info:
                        menor = registro
            if menor:
                usados.add(menor.info)
                dados_ordenados.append(dados[menor.index])

        return [cidade.to_dict() for cidade in dados_ordenados]

    def carregar_arvore_binaria(self) -> ArvoreBinaria:
        return ArvoreBinaria.construir_arvore(self.buscar_todas_cidades())
