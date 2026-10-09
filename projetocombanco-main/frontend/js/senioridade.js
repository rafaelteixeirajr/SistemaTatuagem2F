// endereço da nossa API backend
const API = 'http://127.0.0.1:8000'

// elementos do formulário e do botão de enviar
const formSenioridade = document.getElementById('form-senioridade')
const botaoSubmit = document.getElementById('btn-submit-senioridade')

// limpa o formulário e devolve o botão para o modo de cadastro
function limparFormulario() {
  formSenioridade.reset()
  delete formSenioridade.dataset.idSenioridade
  botaoSubmit.textContent = 'Cadastrar'
  botaoSubmit.classList.remove('btn-success')
  botaoSubmit.classList.add('btn-primary')
}

// ─── Carrega a lista de senioridades ao abrir a página ───
async function listarSenioridades() {
  const resposta = await fetch(`${API}/senioridade`)
  const senioridades = await resposta.json()

  const corpo = document.getElementById('corpo-tabela')
  corpo.innerHTML = ''

  senioridades.forEach(s => {
    corpo.innerHTML += `
      <tr>
        <td>${s.idsenioridade}</td>
        <td>${s.nome}</td>
        <td>
          <button class="btn btn-sm btn-warning me-2" onclick='preencherFormularioEdicao(${JSON.stringify(s)})'>Editar</button>
          <button class="btn btn-sm btn-danger" onclick="deletarSenioridade(${s.idsenioridade})">Excluir</button>
        </td>
      </tr>`
  })
}

listarSenioridades()

// ─── Cadastrar e atualizar senioridades ───
formSenioridade.addEventListener('submit', async (e) => {
  e.preventDefault()

  const senioridade = { nome: document.getElementById('nome').value }
  const idSenioridade = formSenioridade.dataset.idSenioridade

  if (idSenioridade) {
    await fetch(`${API}/senioridade/${idSenioridade}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(senioridade)
    })
  } else {
    await fetch(`${API}/senioridade`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(senioridade)
    })
  }

  limparFormulario()
  listarSenioridades()
})

// ─── Abre os dados da senioridade no formulário para edição ───
function preencherFormularioEdicao(senioridade) {
  document.getElementById('nome').value = senioridade.nome
  formSenioridade.dataset.idSenioridade = senioridade.idsenioridade

  botaoSubmit.textContent = 'Salvar alteração'
  botaoSubmit.classList.remove('btn-primary')
  botaoSubmit.classList.add('btn-success')
}

// ─── Exclui uma senioridade ───
async function deletarSenioridade(id) {
  if (!confirm('Tem certeza que deseja excluir esta senioridade?')) return

  await fetch(`${API}/senioridade/${id}`, { method: 'DELETE' })
  listarSenioridades()
}