document.addEventListener("DOMContentLoaded", () => {
    // SIMULAÇÃO DO BANCO DE DADOS (COMPARTILHADO ENTRE PÁGINAS)

    let db = {
        cidades: JSON.parse(localStorage.getItem("db_cidades")) || [
            {codigo: 1, descricao: "Assis", estado: "SP"},
            {codigo: 2, descricao: "Marília", estado: "SP"},
        ],
        alunos: JSON.parse(localStorage.getItem("db_alunos")) || [
            {
                codigo: 101,
                nome: "Ana Souza",
                codigo_cidade: 1,
                nascimento: "2002-08-10",
                peso: 60,
                altura: 1.65,
            },
        ],
        professores: JSON.parse(localStorage.getItem("db_professores")) || [
            {
                codigo: 51,
                nome: "Ricardo Borges",
                endereco: "Rua das Flores, 123",
                telefone: "(18) 99999-1111",
                codigo_cidade: 1,
            },
        ],
    };

    //Função para salvar o conteudo incluido:
    function salvarDB() {
        localStorage.setItem("db_cidades", JSON.stringify(db.cidades));
        localStorage.setItem("db_alunos", JSON.stringify(db.alunos));
        localStorage.setItem("db_professores", JSON.stringify(db.professores));
    }

    // FUNÇÕES COMPARTILHADAS

    //Função para adicionar as cidades salvas no select:
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
                .then(response => response.json())  // RETORNAR!
                .then(data => {
                    console.log("Dados recebidos:", data);
                    cidade = data;
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

        function calcularIMC(peso, altura) {
            if (!peso || !altura) return "Dados de peso/altura incompletos.";
            const imc = peso / (altura * altura);
            const diagnostico =
                imc < 18.5
                    ? "Abaixo do peso"
                    : imc < 24.9
                        ? "Peso normal"
                        : imc < 29.9
                            ? "Sobrepeso"
                            : "Obesidade";
            return `IMC: ${imc.toFixed(2)} (${diagnostico})`;
        }

        function renderizarAlunos() {
            alunosTbody.innerHTML = "";
            fetch("/alunos/leitura_exaustiva", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            })
                .then(response => response.json())
                .then(data => {
                    data.forEach((aluno) => {
                        const cidadeDoAluno =
                            db.cidades.find((c) => c.codigo === aluno.codigo_cidade)
                                ?.descricao || "N/A";
                        alunosTbody.innerHTML += `
                    <tr>
                        <td>${aluno.codigo}</td>
                        <td>${aluno.nome}</td>
                        <td>${aluno.codCidade}</td>
                        <td>${new Date(
                            aluno.nascimento + "T00:00:00"
                        ).toLocaleDateString()}</td>
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
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    const lista = document.getElementById("lista-cidades");
                    data.forEach(cidade => {
                        const li = document.createElement("li");
                        li.textContent = `${cidade.codigo} - ${cidade.descricao} (${cidade.estado})`;
                        lista.appendChild(li);
                    });
                })
                .catch(error => console.error("Erro:", error));
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
                .then(response => response.json())  // RETORNAR!
                .then(data => {
                    console.log("Dados recebidos:", data);
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
                const aluno = db.alunos.find((a) => a.codigo === id);
                if (aluno) {
                    alert(
                        `Diagnóstico para ${aluno.nome}:\n${calcularIMC(
                            aluno.peso,
                            aluno.altura
                        )}`
                    );
                }
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
});
