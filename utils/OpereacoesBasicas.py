import json
import os
from typing import Any, List
from enums.TipoRegistro import TipoRegistroEnum
from models.Alunos import Alunos
from models.ArvoresBinaria import ArvoreBinaria
from models.Cidades import Cidades
from models.Matriculas import Matriculas
from models.Modalidades import Modalidades
from models.Professores import Professores

class OperacoesBasicas:
    def __init__(self, tipo_registro: TipoRegistroEnum):
        self.tipo_registro = tipo_registro
        self.arquivo_dados: Any = None
        self.pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        os.makedirs(self.pasta_archives, exist_ok=True)
        self.pasta_indices = os.path.join(self.pasta_archives, 'indices')
        os.makedirs(self.pasta_indices, exist_ok=True)

    import json

    def buscar_todas_cidades(self) -> list[Cidades]:
        cidades = []
        with open(self.arquivo_dados, "r", encoding="utf-8") as arquivo:
            dados_json = json.load(arquivo)
            for d in dados_json:
                cidade = Cidades(
                    codigo=int(d["codigo"]),
                    descricao=d["descricao"],
                    estado=d["estado"]
                )
                cidades.append(cidade)
        return cidades

    def inserir_dados(self, objeto: Cidades | Alunos | Matriculas | Professores | Modalidades):
        match self.tipo_registro:
            case TipoRegistroEnum.ALUNO:
                path_dados = os.path.join(self.pasta_archives, "alunos.txt")
            case TipoRegistroEnum.PROFESSOR:
                path_dados = os.path.join(self.pasta_archives, "professores.txt")
            case TipoRegistroEnum.MODALIDADE:
                path_dados = os.path.join(self.pasta_archives, "modalidades.txt")
            case TipoRegistroEnum.CIDADE:
                path_dados = os.path.join(self.pasta_archives, "cidades.txt")
            case TipoRegistroEnum.MATRICULA:
                path_dados = os.path.join(self.pasta_archives, "matriculas.txt")
            case _:
                raise ValueError("Tipo de registro inválido.")

        if not os.path.exists(path_dados):
            open(path_dados, "w", encoding="utf-8").close()

        print(self.carregar_cidades(path_dados))

        with open(path_dados, 'a', encoding="utf-8") as arquivo:
            arquivo.write(str(objeto) + "\n")

    def converter_para_arvore(self, objetos: list) -> "ArvoreBinaria":
        arvore = ArvoreBinaria()
        arvore.raiz = None
        lista_nos = []
        no_to_index = {}
        def percorrer(no):
            if no is None:
                return
            indice = len(lista_nos)
            lista_nos.append(no)
            no_to_index[no] = indice
            percorrer(no.esquerda)
            percorrer(no.direita)
        for pos, registro in enumerate(objetos):
            arvore.inserir(registro.codigo, pos)
        percorrer(arvore.raiz)
        caminho_arquivo = os.path.join(self.pasta_indices, "CidadesIndices.txt")
        os.makedirs(self.pasta_indices, exist_ok=True)
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            for no in lista_nos:
                esquerda_idx = no_to_index.get(no.esquerda, -1)
                direita_idx = no_to_index.get(no.direita, -1)
                data = {
                    "esquerda": esquerda_idx,
                    "direita": direita_idx,
                    "info": no.codigo,
                    "index": no.index
                }
                f.write(json.dumps(data) + "\n")
        return arvore
