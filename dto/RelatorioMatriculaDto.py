class RelatorioMatriculaDto:
    def __init__(self, codigo=0, nomeAluno='', cidadeAluno='', modalidade='', professor='', valorPagar=0.0):
        self.codigo = codigo
        self.nomeAluno = nomeAluno
        self.cidadeAluno = cidadeAluno
        self.modalidade = modalidade
        self.professor = professor
        self.valorPagar = valorPagar