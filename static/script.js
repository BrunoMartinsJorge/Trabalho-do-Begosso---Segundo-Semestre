document.addEventListener("DOMContentLoaded", () => {

        function carregarCidadesEmSelect(selectId) {
            const selectElement = document.getElementById(selectId);
            if (!selectElement) return;

            selectElement.innerHTML =
                '<option value="" disabled selected>Selecione...</option>';
            fetch("cidades/leitura_exaustiva").then(resp => resp.json()).then((data) => {
                data.forEach((cidade) => {
                    selectElement.innerHTML += `<option value="${cidade.codigo}">${cidade.descricao} - ${cidade.estado}</option>`;
                });
            })
        }

        function carregarProfessoresEmSelect(selectId) {
            const selectElement = document.getElementById(selectId);
            if (!selectElement) return;

            selectElement.innerHTML =
                '<option value="" disabled selected>Selecione...</option>';
            fetch("professores/listar_todos").then(resp => resp.json()).then((data) => {
                data.forEach((professor) => {
                    selectElement.innerHTML += `<option value="${professor.codigo}">${professor.nome}</option>`;
                });
            })
        }

        function carregarModalidadesEmSelect(selectId) {
            const selectElement = document.getElementById(selectId);
            if (!selectElement) return;

            selectElement.innerHTML =
                '<option value="" disabled selected>Selecione...</option>';
            fetch("modalidades/leitura_exaustiva").then(resp => resp.json()).then((data) => {
                data.forEach((professor) => {
                    selectElement.innerHTML += `<option value="${professor.codigo}">${professor.nome}</option>`;
                });
            })
        }


        // LÓGICA DA PÁGINA DE CIDADES

        const cidadesPage = document.getElementById("cidades-form");
        if (cidadesPage) {
            const cidadesTbody = document.getElementById("cidades-tbody");
            const btnBuscar = document.getElementById("btn-buscar");

            function renderizarCidades() {
                cidadesTbody.innerHTML = "";
                fetch(`/cidades/leitura_exaustiva`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    },
                }).then(response => response.json()).then((data) => {
                    data.forEach((cidade) => {
                        cidadesTbody.innerHTML += `
                    <tr>
                        <td>${cidade.codigo}</td>
                        <td>${cidade.descricao}</td>
                        <td>${cidade.estado}</td>
                        <td class="action-buttons">
                            <button class="btn-delete" data-id="${cidade.codigo}" title="Excluir">🗑️</button>
                        </td>
                    </tr>`;
                    });
                })
                    .catch(error => console.error("Erro:", error));
            }

            cidadesPage.addEventListener("submit", (e) => {
                e.preventDefault();
                const formElements = e.target.elements;
                const codigo = parseInt(formElements["cidade-codigo"].value);
                const resultadoDiv = document.getElementById("resultado-busca-cidade");
                resultadoDiv.classList.remove("hidden");
                const novaCidade = {
                    codigo,
                    descricao: formElements["cidade-descricao"].value,
                    estado: formElements["cidade-estado"].value.toUpperCase(),
                };
                resultadoDiv.innerHTML = '';
                fetch("/cidades/cadastrar_cidade", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(novaCidade)
                })
                    .then(async response => {
                        const data = await response.json();
                        if (!response.ok) {
                            resultadoDiv.innerHTML = `❌ Cidade com código #${
                                codigo || "inválido"
                            } já existe.`;
                            throw new Error(data.erro);
                        }
                        cidadesPage.reset();
                        renderizarCidades();
                    })
                    .catch(error => {
                        console.error("Erro:", error);
                    });
            });

            btnBuscar.addEventListener("click", () => {
                const id = parseInt(document.getElementById("busca").value);
                const resultadoDiv = document.getElementById("resultado-busca-cidade");
                resultadoDiv.classList.remove("hidden");
                fetch(`/cidades/buscar_cidade_por_codigo?codigo=${id}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    },
                })
                    .then(response => response.json())
                    .then(data => {
                        const cidade = data;
                        if (cidade) {
                            resultadoDiv.innerHTML = `
                        <strong> Cidade Encontrada:</strong><br>
                        <strong>Código:</strong> #${cidade.codigo}<br>
                        <strong>Descrição:</strong> ${cidade.descricao}<br>
                        <strong>Estado:</strong> ${cidade.estado}
                    `;
                        } else {
                            resultadoDiv.innerHTML = `❌ Aluno com código #${
                                id || "inválido"
                            } não encontrado.`;
                        }
                    })
                    .catch(error => console.error("Erro:", error));
            });

            cidadesTbody.addEventListener("click", (e) => {
                const deleteButton = e.target.closest(".btn-delete");
                if (deleteButton) {
                    const id = parseInt(deleteButton.dataset.id);
                    fetch(`/cidades/apagar_cidades_por_codigo?codigo=${id}`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                    })
                        .then(data => {
                            renderizarCidades();
                        })
                        .catch(error => console.error("Erro:", error));
                }
            });

            renderizarCidades();
        }

        // LÓGICA DA PÁGINA DE ALUNOS

        const alunosPage = document.getElementById("alunos-form");
        if (alunosPage) {
            const alunosTbody = document.getElementById("alunos-tbody");
            const btnBuscar = document.getElementById("btn-buscar");

            function renderizarAlunos() {
                alunosTbody.innerHTML = "";
                fetch("/alunos/buscar_todos", {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    }
                })
                    .then(response => response.json())
                    .then(data => {
                        data.forEach((aluno) => {
                            const dataNasc = aluno.dataNascimento
                                ? formatDateLocal(aluno.dataNascimento)
                                : "Data não informada";
                            alunosTbody.innerHTML += `
                    <tr>
                        <td>${aluno.codigo}</td>
                        <td>${aluno.nome}</td>
                        <td>${aluno.cidade}</td>
                        <td>${dataNasc}</td>
                        <td class="action-buttons">
                            <button class="btn-info" data-id="${
                                aluno.codigo
                            }" title="Ver IMC">📊</button>
                            <button class="btn-delete" data-id="${
                                aluno.codigo
                            }" title="Excluir">🗑️</button>
                        </td>
                    </tr>`;
                        });
                    })
                    .catch(error => console.error("Erro:", error));
            }

            alunosPage.addEventListener("submit", (e) => {
                e.preventDefault();
                const formElements = e.target.elements;
                const codigo = parseInt(formElements["aluno-codigo"].value);
                const resultadoDiv = document.getElementById("resultado-busca-aluno");
                const novoAluno = {
                    codigo,
                    nome: formElements["aluno-nome"].value,
                    codigo_cidade: parseInt(formElements["aluno-cidade"].value),
                    nascimento: formElements["aluno-nascimento"].value,
                    peso: parseFloat(formElements["aluno-peso"].value),
                    altura: parseFloat(formElements["aluno-altura"].value),
                };
                fetch("/alunos/cadastrar_aluno", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(novoAluno)
                })
                    .then(async response => {
                            const data = await response.json();
                            if (!response.ok) {
                                resultadoDiv.classList.remove("hidden");
                                resultadoDiv.innerHTML = `❌ ${data.erro}`;
                                throw new Error(data.erro);
                            }
                            const lista = document.getElementById("lista-cidades");
                            data.forEach(cidade => {
                                const li = document.createElement("li");
                                li.textContent = `${cidade.codigo} - ${cidade.descricao} (${cidade.estado})`;
                                lista.appendChild(li);
                            });
                        }
                    ).catch(error => console.error("Erro:", error));
                alunosPage.reset();
                renderizarAlunos();
            });

            btnBuscar.addEventListener("click", () => {
                const id = parseInt(document.getElementById("busca").value);
                const resultadoDiv = document.getElementById("resultado-busca-aluno");
                let aluno;
                resultadoDiv.classList.remove("hidden");
                fetch(`/alunos/buscar_aluno_por_codigo?codigo=${id}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    },
                })
                    .then(response => response.json())
                    .then(data => {
                        aluno = data;
                        if (aluno) {
                            resultadoDiv.innerHTML = `
                    <strong> Aluno Encontrado:</strong><br>
                    <strong>Código:</strong> #${aluno.aluno.codigo} - ${aluno.aluno.nome}<br>
                    <strong>Cidade:</strong> ${aluno.cidade.nome} - ${aluno.cidade.estado}<br>
                    <strong>Diagnóstico Corporal:</strong> ${aluno.imc}
                `;
                        } else {
                            resultadoDiv.innerHTML = `❌ Aluno com código #${
                                id || "inválido"
                            } não encontrado.`;
                        }
                    })
                    .catch(error => console.error("Erro:", error));
            });

            alunosTbody.addEventListener("click", (e) => {
                const button = e.target.closest("button");
                if (!button) return;
                const id = parseInt(button.dataset.id);

                if (button.matches(".btn-delete")) {
                    fetch(`/alunos/apagar_alunos_por_codigo?codigo=${id}`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                    })
                        .then(data => {
                            renderizarAlunos();
                        })
                        .catch(error => console.error("Erro:", error));
                }
                if (button.matches(".btn-info")) {
                    fetch(`/alunos/calcular_imc?codigo=${id}`, {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json"
                        },
                    })
                        .then(async data => {
                            const aluno = await data.json();
                            alert(
                                `Diagnóstico para ${aluno.nome}:\n${aluno.imc}`
                            );
                        })
                        .catch(error => console.error("Erro:", error));
                }
            });

            carregarCidadesEmSelect("aluno-cidade");
            renderizarAlunos();
        }

        // LÓGICA DA PÁGINA DE PROFESSORES

        const professoresPage = document.getElementById("professores-form");
        if (professoresPage) {
            const professoresTbody = document.getElementById("professores-tbody");
            const btnBuscar = document.getElementById("btn-buscar");

            function renderizarProfessores() {
                professoresTbody.innerHTML = "";
                fetch(`/professores/listar_todos`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    },
                }).then(response => response.json()).then((data) => {
                    data.forEach((professor) => {
                        professoresTbody.innerHTML += `
                    <tr>
                        <td>${professor.codigo}</td>
                        <td>${professor.nome}</td>
                        <td>${professor.endereco}</td>
                        <td>${professor.telefone}</td>
                        <td>${professor.cidade}</td>
                        <td class="action-buttons">
                            <button class="btn-delete" data-id="${professor.codigo}" title="Excluir">🗑️</button>
                        </td>
                    </tr>`;
                    })
                });
            }

            professoresPage.addEventListener("submit", (e) => {
                e.preventDefault();
                const formElements = e.target.elements;
                const codigo = parseInt(formElements["professor-codigo"].value);
                const resultadoDiv = document.getElementById("resultado-busca-professor");
                resultadoDiv.classList.remove("hidden");
                const novoProfessor = {
                    codigo,
                    nome: formElements["professor-nome"].value,
                    endereco: formElements["professor-endereco"].value,
                    telefone: formElements["professor-telefone"].value,
                    codigo_cidade: parseInt(formElements["professor-cidade"].value),
                };
                fetch("/professores/cadastrar_profesor", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(novoProfessor)
                })
                    .then(async response => {
                        const data = await response.json();
                        if (!response.ok) {
                            resultadoDiv.innerHTML = `❌ Professor com código #${
                                codigo || "inválido"
                            } já existe.`;
                            throw new Error(data.erro);
                        }
                        professoresPage.reset();
                        renderizarProfessores();
                    })
                    .catch(error => {
                        console.error("Erro:", error);
                    });
            });

            btnBuscar.addEventListener("click", () => {
                const id = parseInt(document.getElementById("busca").value);
                let professor;
                const resultadoDiv = document.getElementById("resultado-busca-professor");
                resultadoDiv.classList.remove("hidden");

                fetch(`/professores/buscar_professor_por_codigo?codigo=${id}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    },
                })
                    .then(response => response.json())
                    .then(data => {
                        professor = data
                        if (professor) {
                            resultadoDiv.innerHTML = `
                    <strong> Professor Encontrado:</strong><br>
                    <strong>Código:</strong> #${professor.professor.codigo} - ${professor.professor.nome}<br>
                    <strong>Endereço:</strong> ${professor.professor.endereco}<br>
                    <strong>Telefone:</strong> ${professor.professor.telefone}<br>
                    <strong>Cidade:</strong> ${professor.cidade.nome} - ${professor.cidade.estado}
                 `;
                        } else {
                            resultadoDiv.innerHTML = `❌ Professor com código #${
                                id || "inválido"
                            } não encontrado.`;
                        }
                    });
            });

            professoresTbody.addEventListener("click", (e) => {
                const deleteButton = e.target.closest(".btn-delete");
                if (deleteButton) {
                    const id = parseInt(deleteButton.dataset.id);
                    fetch(`/professores/apagar_profesor_por_codigo?codigo=${id}`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                    })
                        .then(data => {
                            renderizarProfessores();
                        })
                        .catch(error => console.error("Erro:", error));
                }
            });

            carregarCidadesEmSelect("professor-cidade");
            renderizarProfessores();
        }

        const modalidadesPage = document.getElementById("modalidades-form");
        if (modalidadesPage) {
            const modalidadesTbody = document.getElementById("modalidades-tbody");
            const btnBuscar = document.getElementById("btn-buscar");

            function renderizarModalidades() {
                modalidadesTbody.innerHTML = "";
                fetch(`/modalidades/lista_tabela`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    },
                }).then(response => response.json()).then((data) => {
                    data.forEach((professor) => {
                        modalidadesTbody.innerHTML += `
                    <tr>
                        <td>${professor.codigo}</td>
                        <td>${professor.descricao}</td>
                        <td>${professor.professor}</td>
                        <td>${professor.valorAula}</td>
                        <td>${professor.limite}</td>
                        <td>${professor.totalMatriculados} Matriculado(s)</td>
                        <td class="action-buttons">
                            <button class="btn-delete" data-id="${professor.codigo}" title="Excluir">🗑️</button>
                        </td>
                    </tr>`;
                    })
                });
            }

            modalidadesPage.addEventListener("submit", (e) => {
                e.preventDefault();
                const formElements = e.target.elements;
                const codigo = parseInt(formElements["modalidade-codigo"].value);
                const resultadoDiv = document.getElementById("resultado-busca-modalidade");
                resultadoDiv.classList.remove("hidden");
                const novaModalidade = {
                    codigo,
                    descricao: formElements["modalidade-descricao"].value,
                    professor: formElements["modalidade-professor"].value,
                    valorAula: formElements["modalidade-valor"].value,
                    limite: parseInt(formElements["modalidade-limite"].value),
                };
                fetch("/modalidades/cadastrar_modalidade", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(novaModalidade)
                })
                    .then(async response => {
                        const data = await response.json();
                        if (!response.ok) {
                            resultadoDiv.innerHTML = `❌ Professor com código #${
                                codigo || "inválido"
                            } já existe.`;
                            throw new Error(data.erro);
                        }
                        modalidadesPage.reset();
                        renderizarModalidades();
                    })
                    .catch(error => {
                        console.error("Erro:", error);
                    });
            });

            btnBuscar.addEventListener("click", () => {
                const id = parseInt(document.getElementById("busca").value);
                let professor;
                const resultadoDiv = document.getElementById("resultado-busca-modalidade");
                resultadoDiv.classList.remove("hidden");

                fetch(`/modalidades/buscar_modalidade_por_codigo?codigo=${id}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    },
                })
                    .then(response => response.json())
                    .then(data => {
                        modalidade = data
                        if (modalidade) {
                            resultadoDiv.innerHTML = `
                    <strong> Modalidade Encontrada:</strong><br>
                    <strong>Código:</strong> #${modalidade.modalidade.codigo}<br>
                    <strong>Descrição:</strong> ${modalidade.modalidade.descricao}<br>
                    <strong>Professor:</strong> ${modalidade.info.professor} - ${modalidade.info.cidade}<br>
                    <strong>Valor da Aula:</strong> R$ ${modalidade.modalidade.valorDaAula}<br>
                    <strong>Limite de Alunos:</strong> ${modalidade.modalidade.limiteAlunos}<br>
                    <strong>Total de Matriculas:</strong> ${modalidade.modalidade.totalMatriculas}<br>
                 `;
                        } else {
                            resultadoDiv.innerHTML = `❌ Professor com código #${
                                id || "inválido"
                            } não encontrado.`;
                        }
                    });
            });

            modalidadesTbody.addEventListener("click", (e) => {
                const deleteButton = e.target.closest(".btn-delete");
                if (deleteButton) {
                    const id = parseInt(deleteButton.dataset.id);
                    fetch(`/modalidades/apagar_modalidades_por_codigo?codigo=${id}`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                    })
                        .then(data => {
                            renderizarModalidades();
                        })
                        .catch(error => console.error("Erro:", error));
                }
            });

            carregarProfessoresEmSelect("modalidade-professor");
            renderizarModalidades();
        }

        const relatorioPage = document.getElementById("form-faturamento");
        if (relatorioPage) {
            const modalidadesSelect = document.getElementById("faturamento-modalidade");
            const modalidadesMatriculasSelect = document.getElementById("modalidade-matriculas");
            const resultadoFaturamento = document.getElementById("resultado-faturamento");
            const btnRelatorioGeral = document.getElementById("btn-relatorio-geral");
            const relatorioGeralTbody = document.getElementById("relatorioGeralTbody");
            const relatorioGeralTotais = document.getElementById("relatorio-geral-totais");

            function calcularFaturamentoModalidade(listaMatriculados) {
                let soma = 0;
                listaMatriculados.forEach((matriculado) => {
                    soma += matriculado.valorPagar;
                })
                return soma;
            }

            // Carregar modalidades no select
            function carregarModalidadesEmSelect() {
                modalidadesSelect.innerHTML = `<option value="" disabled selected>Selecione...</option>`;
                modalidadesMatriculasSelect.innerHTML = `<option value="" disabled selected>Selecione...</option>`;
                fetch("/modalidades/lista_tabela", {
                    method: "GET",
                    headers: {"Content-Type": "application/json"},
                })
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(modalidade => {
                            modalidadesSelect.innerHTML += `
                        <option value="${modalidade.codigo}">
                            ${modalidade.descricao} - Prof. ${modalidade.professor}
                        </option>
                    `;
                            modalidadesMatriculasSelect.innerHTML += `
                        <option value="${modalidade.codigo}">
                            ${modalidade.descricao} - Prof. ${modalidade.professor}
                        </option>
                    `;
                        });
                    })
                    .catch(error => console.error("Erro ao carregar modalidades:", error));
            }

            // Relatório de faturamento por modalidade
            relatorioPage.addEventListener("submit", (e) => {
                e.preventDefault();
                const codigo = modalidadesSelect.value;

                if (!codigo) return;

                fetch(`/modalidades/buscar_faturamento?codigo=${codigo}`, {
                    method: "GET",
                    headers: {"Content-Type": "application/json"},
                })
                    .then(response => response.json())
                    .then(data => {
                        resultadoFaturamento.classList.remove("hidden");
                        resultadoFaturamento.innerHTML = `
                    <h4>📊 Relatório de Faturamento</h4>
                    <p><strong>Modalidade:</strong> ${data.faturamento.descricao}</p>
                    <p><strong>Nome do Professor:</strong> ${data.faturamento.nome_professor}</p>
                    <p><strong>Cidade do Professor:</strong> ${data.faturamento.cidade_professor}</p>
                    <p><strong>Faturamento Total:</strong> R$ ${data.faturamento.valor_faturado}</p>
                `;
                    })
                    .catch(error => {
                        console.error("Erro ao gerar relatório:", error);
                        resultadoFaturamento.classList.remove("hidden");
                        resultadoFaturamento.innerHTML = `❌ Erro ao gerar relatório.`;
                    });
            });

            // Relatório geral de matrículas
            btnRelatorioGeral.addEventListener("click", (e) => {
                e.preventDefault(); // evita recarregar a página

                const codigo = modalidadesMatriculasSelect.value; // usa o select correto
                if (!codigo) return;

                fetch(`/relatorio/listar-relatorio-matriculas?codigo=${codigo}`, {
                    method: "GET",
                    headers: {"Content-Type": "application/json"},
                })
                    .then(response => response.json())
                    .then(data => {
                        relatorioGeralTbody.innerHTML = "";
                        let total = 0;

                        data.forEach(matricula => {
                            relatorioGeralTbody.innerHTML += `
                    <tr>
                        <td>${matricula.codigo}</td>
                        <td>${matricula.nomeAluno}</td>
                        <td>${matricula.cidadeAluno}</td>
                        <td>${matricula.modalidade}</td>
                        <td>${matricula.professor}</td>
                        <td>R$ ${matricula.valorPagar}</td>
                    </tr>
                `;
                        });
                        relatorioGeralTotais.classList.remove("hidden");
                        relatorioGeralTotais.innerHTML = `
                <h4>📈 Totais</h4>
                <p><strong>Total de Matrículas:</strong> ${data.length}</p>
                <p><strong>Faturamento Total:</strong> R$ ${calcularFaturamentoModalidade(data)}</p>
            `;
                    })
                    .catch(error => console.error("Erro ao carregar relatório geral:", error));
            });

            // Inicializar selects
            carregarModalidadesEmSelect();
        }
    }
)
;

function formatDateLocal(iso) {
    if (!iso) return '';
    const [year, month, day] = iso.split('-');
    return new Date(year, month - 1, day).toLocaleDateString('pt-BR');
}