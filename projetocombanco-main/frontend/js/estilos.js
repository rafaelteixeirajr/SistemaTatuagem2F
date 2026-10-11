const API = 'http://127.0.0.1:8000'
const formEstilo = document.getElementById('form-estilo')
const botaoSubmit = document.getElementById('btn-submit-estilo')

function limparFormulario() {
  formEstilo.reset()
  delete formEstilo.dataset.idEstilo
  botaoSubmit.textContent = 'Cadastrar'
  botaoSubmit.classList.remove('btn-success')
  botaoSubmit.classList.add('btn-primary')
}

async function listarEstilos() {
  const resposta = await fetch(`${API}/estilos`)
  const estilos = await resposta.json()

  const corpo = document.getElementById('corpo-tabela')
  corpo.innerHTML = ''

  estilos.forEach(e => {
    corpo.innerHTML += `
      <tr>
        <td>${e.idestilo}</td>
        <td>${e.descricao}</td>
        <td>
          <button class="btn btn-sm btn-warning me-2" onclick='preencherFormularioEdicao(${JSON.stringify(e)})'>Editar</button>
          <button class="btn btn-sm btn-danger" onclick="deletarEstilo(${e.idestilo})">Excluir</button>
        </td>
      </tr>`
  })
}

listarEstilos()

formEstilo.addEventListener('submit', async (e) => {
  e.preventDefault()

  const estilo = { descricao: document.getElementById('descricao').value }
  const idEstilo = formEstilo.dataset.idEstilo

  if (idEstilo) {
    await fetch(`${API}/estilos/${idEstilo}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(estilo)
    })
  } else {
    await fetch(`${API}/estilos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(estilo)
    })
  }

  limparFormulario()
  listarEstilos()
})

function preencherFormularioEdicao(estilo) {
  document.getElementById('descricao').value = estilo.descricao
  formEstilo.dataset.idEstilo = estilo.idestilo
  botaoSubmit.textContent = 'Salvar alteração'
  botaoSubmit.classList.remove('btn-primary')
  botaoSubmit.classList.add('btn-success')
}

async function deletarEstilo(id) {
  if (!confirm('Tem certeza que deseja excluir este estilo?')) return
  await fetch(`${API}/estilos/${id}`, { method: 'DELETE' })
  listarEstilos()
}