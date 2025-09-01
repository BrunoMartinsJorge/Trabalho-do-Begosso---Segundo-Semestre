from typing import Any
import os

from enums.TipoRegistro import TipoRegistroEnum
from models.Alunos import Aluno
from models.ArvoresBinaria import ArvoreBinaria
from models.Cidades import Cidades
from models.Matriculas import Matriculas
from models.Modalidades import Modalidades
from models.Professores import Professores


class OperacoesBasicas:
    def incluir_novo_registro(self, tipo_de_registro: TipoRegistroEnum, novo_registro: Any):
        pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        os.makedirs(pasta_archives, exist_ok=True)
        pasta_indices = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives/indices')
        os.makedirs(pasta_indices, exist_ok=True)

        match tipo_de_registro:
            case TipoRegistroEnum.ALUNO:
                novo_obj = Aluno(
                    novo_registro.codigo,
                    novo_registro.nome,
                    novo_registro.codCidade,
                    novo_registro.nascimento,
                    novo_registro.peso,
                    novo_registro.altura,
                    novo_registro.status
                )
                arquivo_path = os.path.join(pasta_archives, 'Alunos.txt')
                arquivo_indices_path = os.path.join(pasta_indices, 'AlunosIndices.txt')
            case TipoRegistroEnum.PROFESSOR:
                novo_obj = Professores(
                    novo_registro.codigo,
                    novo_registro.nome,
                    novo_registro.endereco,
                    novo_registro.telefone,
                    novo_registro.codCidade,
                )
                arquivo_path = os.path.join(pasta_archives, 'Professores.txt')
                arquivo_indices_path = os.path.join(pasta_indices, 'ProfessoresIndices.txt')
            case TipoRegistroEnum.CIDADE:
                novo_obj = Cidades(
                    novo_registro.codigo,
                    novo_registro.descricao,
                    novo_registro.estado,
                )
                if self.verificar_se_objeto_ja_existe(TipoRegistroEnum.CIDADE, novo_obj):
                    print(f"Registro de cidade {novo_obj.codigo} já existe.")
                    return
                arquivo_path = os.path.join(pasta_archives, 'Cidades.txt')
                arquivo_indices_path = os.path.join(pasta_indices, 'CidadesIndices.txt')
            case TipoRegistroEnum.MODALIDADE:
                novo_obj = Modalidades(
                    novo_registro.codigo,
                    novo_registro.descricao,
                    novo_registro.codProfessor,
                    novo_registro.valorDaAula,
                    novo_registro.limiteAlunos,
                    novo_registro.totalMatriculas
                )
                arquivo_path = os.path.join(pasta_archives, 'Modalidades.txt')
                arquivo_indices_path = os.path.join(pasta_indices, 'ModalidadesIndices.txt')
            case TipoRegistroEnum.MATRICULA:
                novo_obj = Matriculas(
                    novo_registro.codigo,
                    novo_registro.codAluno,
                    novo_registro.codModalidade,
                    novo_registro.quantidadeAulas,
                )
                arquivo_path = os.path.join(pasta_archives, 'Matriculas.txt')
                arquivo_indices_path = os.path.join(pasta_indices, 'MatriculasIndices.txt')
            case _:
                raise ValueError(f"Tipo de registro desconhecido: {tipo_de_registro}")

        with open(arquivo_path, 'a', encoding='utf-8') as arquivo:
            arquivo.write(str(novo_obj) + "\n")
        lista_objetos = self.transformar_arquivo_em_objeto(arquivo_indices_path)
        self.incluir_na_arvore(novo_obj, 0, lista_objetos, len(lista_objetos), tipo_de_registro)

    '''def incluir_na_arvore(self, novo_registro: Any, raiz, indices, quantidade_itens, tipo_registros: TipoRegistroEnum):
        codigo = novo_registro.codigo
        atual = raiz
        pai = -1
        direcao = None
        while atual != 0:
            parte = indices[atual]
            if codigo == parte.info:
                return parte.index
            pai = atual
            if codigo < parte.info:
                direcao = 'esquerda'
                atual = parte.esquerda
            else:
                direcao = 'direita'
                atual = parte.direita
        novo_index = len(indices)
        novo_no = ArvoreBinaria(0, 0, codigo, quantidade_itens)
        indices.append(novo_no)
        if direcao == 'esquerda':
            indices[pai].esquerda = novo_index
        elif direcao == 'direita':
            indices[pai].direita = novo_index
        self.__incluir_novo_arquivo(tipo_registros, str(novo_no))
        return novo_no.index'''

    def incluir_na_arvore(self, novo_registro: Any, raiz, indices: Any, qtd_intens: int, tipo_registro: TipoRegistroEnum):
        codigo = novo_registro.codigo
        atual = raiz
        pai = -1
        direcao = None
        while atual != 0:
            parte = indices[atual]
            if codigo == parte.info:
                return parte.index
            pai = atual
            if codigo < parte.info:
                direcao = 'esquerda'
                atual = parte.esquerda
            else:
                direcao = 'direita'
                atual = parte.direita
        novo_index = len(indices)
        novo_no = ArvoreBinaria(0, 0, codigo, qtd_intens - 1)
        self.__incluir_novo_arquivo(tipo_registro, str(novo_no))
        if direcao == 'esquerda':
            indices[pai].esquerda = novo_index
        elif direcao == 'direita':
            indices[pai].direita = novo_index
        return novo_no.index

    @staticmethod
    def __incluir_novo_arquivo(tipo_registro: TipoRegistroEnum, novo_no: str):
        pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives/indices')
        os.makedirs(pasta_archives, exist_ok=True)

        match tipo_registro:
            case TipoRegistroEnum.CIDADE:
                arquivo_path = os.path.join(pasta_archives, 'CidadesIndices.txt')
            case TipoRegistroEnum.PROFESSOR:
                arquivo_path = os.path.join(pasta_archives, 'ProfessoresIndices.txt')
            case TipoRegistroEnum.MATRICULA:
                arquivo_path = os.path.join(pasta_archives, 'MatriculasIndices.txt')
            case TipoRegistroEnum.MODALIDADE:
                arquivo_path = os.path.join(pasta_archives, 'ModalidadesIndices.txt')
            case TipoRegistroEnum.ALUNO:
                arquivo_path = os.path.join(pasta_archives, 'AlunosIndices.txt')
            case _:
                raise ValueError(f"Tipo de registro desconhecido: {tipo_registro}")

        with open(arquivo_path, 'a', encoding='utf-8') as arquivo:
            arquivo.write(novo_no + "\n")

    @staticmethod
    def transformar_arquivo_em_objeto(arquivo_path: str) -> list[dict]:
        objetos = []
        with open(arquivo_path, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue
                partes = linha.replace(';', ',').split(',')
                novoObjeto = {}
                for parte in partes:
                    if ':' in parte:
                        chave, valor = parte.split(':', 1)
                        chave = chave.strip().lower()
                        valor = valor.strip()
                        novoObjeto[chave] = valor
                objetos.append(novoObjeto)
        return objetos

    def verificar_se_objeto_ja_existe(self, tipo_de_registro: TipoRegistroEnum, registro: Any) -> bool:
        pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        os.makedirs(pasta_archives, exist_ok=True)
        arquivos = {
            TipoRegistroEnum.CIDADE: 'CidadesIndices.txt',
            TipoRegistroEnum.ALUNO: 'Alunos.txt',
            TipoRegistroEnum.PROFESSOR: 'Professores.txt',
            TipoRegistroEnum.MODALIDADE: 'Modalidades.txt',
            TipoRegistroEnum.MATRICULA: 'Matriculas.txt'
        }
        arquivo_nome = arquivos.get(tipo_de_registro)
        if not arquivo_nome:
            raise ValueError(f"Tipo de registro desconhecido: {tipo_de_registro}")

        arquivo_path = os.path.join(pasta_archives, arquivo_nome)
        if not os.path.exists(arquivo_path):
            return False
        lista_objetos = self.transformar_arquivo_em_objeto(arquivo_path)
        for obj in lista_objetos:
            if obj.get("codigo") == registro.codigo:
                return True
        return False
