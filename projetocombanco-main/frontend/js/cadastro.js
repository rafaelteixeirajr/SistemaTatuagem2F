const API = 'http://127.0.0.1:8000'
const formCadastro = document.getElementById('form-cadastro')

formCadastro.addEventListener('submit', async (e) => {
  e.preventDefault()

  const usuario = {
    nome: document.getElementById('nome').value,
    email: document.getElementById('email').value,
    senha: document.getElementById('senha').value
  }

  const resposta = await fetch(`${API}/usuarios`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(usuario)
  })

  if (resposta.ok) {
    alert('Cadastro feito com sucesso!')
    window.location.href = 'index.html'
    // manda pra Landing Page por enquanto — a tela de login de verdade
    // só vai existir a partir da Aula 15
  } else {
    const erro = await resposta.json()
    alert('Erro ao cadastrar: ' + JSON.stringify(erro))
  }
})