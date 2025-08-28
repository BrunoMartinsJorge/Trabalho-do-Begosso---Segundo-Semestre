fetch("/buscar")
  .then(response => response.json())
  .then(alunos => {
    console.log(alunos);
  })
  .catch(err => console.error("Erro ao buscar alunos:", err));