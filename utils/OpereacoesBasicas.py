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
    def incluir_novo_registro(self, tipoDeRegistro: TipoRegistroEnum, novoRegistro: Any):
        pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        os.makedirs(pasta_archives, exist_ok=True)

        match tipoDeRegistro:
            case TipoRegistroEnum.ALUNO:
                novo_obj = Aluno(
                    novoRegistro.codigo,
                    novoRegistro.nome,
                    novoRegistro.codCidade,
                    novoRegistro.nascimento,
                    novoRegistro.peso,
                    novoRegistro.altura,
                    novoRegistro.status
                )
                arquivo_path = os.path.join(pasta_archives, 'Alunos.txt')

            case TipoRegistroEnum.PROFESSOR:
                novo_obj = Professores(
                    novoRegistro.codigo,
                    novoRegistro.nome,
                    novoRegistro.endereco,
                    novoRegistro.telefone,
                    novoRegistro.codCidade,
                )
                arquivo_path = os.path.join(pasta_archives, 'Professores.txt')

            case TipoRegistroEnum.CIDADE:
                novo_obj = Cidades(
                    novoRegistro.codigo,
                    novoRegistro.descricao,
                    novoRegistro.estado,
                )
                if self.verificar_se_objeto_ja_existe(TipoRegistroEnum.CIDADE, novo_obj):
                    print(f"Registro de cidade {novo_obj.codigo} já existe.")
                    return
                arquivo_path = os.path.join(pasta_archives, 'Cidades.txt')

            case TipoRegistroEnum.MODALIDADE:
                novo_obj = Modalidades(
                    novoRegistro.codigo,
                    novoRegistro.descricao,
                    novoRegistro.codProfessor,
                    novoRegistro.valorDaAula,
                    novoRegistro.limiteAlunos,
                    novoRegistro.totalMatriculas
                )
                arquivo_path = os.path.join(pasta_archives, 'Modalidades.txt')

            case TipoRegistroEnum.MATRICULA:
                novo_obj = Matriculas(
                    novoRegistro.codigo,
                    novoRegistro.codAluno,
                    novoRegistro.codModalidade,
                    novoRegistro.quantidadeAulas,
                )
                arquivo_path = os.path.join(pasta_archives, 'Matriculas.txt')

            case _:
                raise ValueError(f"Tipo de registro desconhecido: {tipoDeRegistro}")

        with open(arquivo_path, 'a', encoding='utf-8') as arquivo:
            arquivo.write(str(novo_obj) + "\n")

    def incluir_na_arvore(self, arvore: int, novoCod: int, novoIndex: int, indices: list[ArvoreBinaria]):
        atual = arvore
        pai = -1
        direcao = None
        while atual != 0:
            parte = indices[atual]
            if novoCod == parte.info:
                return parte.index
            pai = atual
            if novoCod < parte.info:
                direcao = "esquerda"
                atual = parte.esquerda
            else:
                direcao = "direita"
                atual = parte.direita

        novo_no_index = len(indices)
        novo_no = ArvoreBinaria(0, 0, novoCod, novoIndex)
        indices.append(novo_no)

        if pai != -1:
            if direcao == "esquerda":
                indices[pai].esquerda = novo_no_index
            else:
                indices[pai].direita = novo_no_index

        return novo_no.index

    def incluir_novo_arquivo(self, tipoDeRegistro: TipoRegistroEnum, novoNo: str):
        pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        os.makedirs(pasta_archives, exist_ok=True)

        match tipoDeRegistro:
            case TipoRegistroEnum.CIDADE:
                arquivo_path = os.path.join(pasta_archives, 'Cidades.txt')
            case TipoRegistroEnum.PROFESSOR:
                arquivo_path = os.path.join(pasta_archives, 'Professores.txt')
            case TipoRegistroEnum.MATRICULA:
                arquivo_path = os.path.join(pasta_archives, 'Matriculas.txt')
            case TipoRegistroEnum.MODALIDADE:
                arquivo_path = os.path.join(pasta_archives, 'Modalidades.txt')
            case TipoRegistroEnum.ALUNO:
                arquivo_path = os.path.join(pasta_archives, 'Alunos.txt')
            case _:
                raise ValueError(f"Tipo de registro desconhecido: {tipoDeRegistro}")

        with open(arquivo_path, 'a', encoding='utf-8') as arquivo:
            arquivo.write(novoNo + "\n")

    def transformar_arquivo_em_objeto(self, arquivoPath: str) -> list[dict]:
        objetos = []
        with open(arquivoPath, 'r', encoding='utf-8') as arquivo:
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

    def verificar_se_objeto_ja_existe(self, tipoDeRegistro: TipoRegistroEnum, registro: Any) -> bool:
        pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        os.makedirs(pasta_archives, exist_ok=True)
        arquivos = {
            TipoRegistroEnum.CIDADE: 'Cidades.txt',
            TipoRegistroEnum.ALUNO: 'Alunos.txt',
            TipoRegistroEnum.PROFESSOR: 'Professores.txt',
            TipoRegistroEnum.MODALIDADE: 'Modalidades.txt',
            TipoRegistroEnum.MATRICULA: 'Matriculas.txt'
        }
        arquivo_nome = arquivos.get(tipoDeRegistro)
        if not arquivo_nome:
            raise ValueError(f"Tipo de registro desconhecido: {tipoDeRegistro}")

        arquivo_path = os.path.join(pasta_archives, arquivo_nome)
        if not os.path.exists(arquivo_path):
            return False
        lista_objetos = self.transformar_arquivo_em_objeto(arquivo_path)
        registro_dict = {k.lower(): str(v).strip() for k, v in registro.__dict__.items()}
        for obj in lista_objetos:
            for chave, valor in registro_dict.items():
                if chave in obj and obj[chave] == valor:
                    return True
        return False
