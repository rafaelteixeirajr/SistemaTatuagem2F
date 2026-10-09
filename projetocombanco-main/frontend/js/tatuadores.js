// endereço da nossa API backend
const API = 'http://127.0.0.1:8000'

// elementos do formulário e do botão de enviar
const formTatuador = document.getElementById('form-tatuador')
const botaoSubmit = document.getElementById('btn-submit-tatuador')

// limpa o formulário e devolve o botão para o modo de cadastro
function limparFormulario() {
  formTatuador.reset()
  delete formTatuador.dataset.idTatuador
  botaoSubmit.textContent = 'Cadastrar'
  botaoSubmit.classList.remove('btn-success')
  botaoSubmit.classList.add('btn-primary')
}

// ─── Busca as senioridades na API e preenche o <select> ───
async function carregarSenioridades() {
  const resposta = await fetch(`${API}/senioridade`)
  const senioridades = await resposta.json()

  const select = document.getElementById('idsenioridade')
  select.innerHTML = '<option value="">Senioridade...</option>'

  senioridades.forEach(s => {
    select.innerHTML += `<option value="${s.idsenioridade}">${s.nome}</option>`
  })
}

carregarSenioridades()

// ─── Carrega a lista de tatuadores ao abrir a página ───
async function listarTatuadores() {
  const resposta = await fetch(`${API}/tatuadores`)
  const tatuadores = await resposta.json()

  const corpo = document.getElementById('corpo-tabela')
  corpo.innerHTML = ''

  tatuadores.forEach(t => {
    corpo.innerHTML += `
      <tr>
        <td>${t.idtatuador}</td>
        <td>${t.nometatuador}</td>
        <td>${t.cpf}</td>
        <td>${t.email ?? '-'}</td>
        <td>${t.telefone ?? '-'}</td>
        <td>${t.senioridade}</td>
        <td>
          <button class="btn btn-sm btn-warning me-2" onclick='preencherFormularioEdicao(${JSON.stringify(t)})'>Editar</button>
          <button class="btn btn-sm btn-danger" onclick="deletarTatuador(${t.idtatuador})">Excluir</button>
        </td>
      </tr>`
  })
}

listarTatuadores()

// ─── Cadastrar e atualizar tatuadores ───
formTatuador.addEventListener('submit', async (e) => {
  e.preventDefault()

  const tatuador = {
    nometatuador: document.getElementById('nometatuador').value,
    cpf: document.getElementById('cpf').value,
    email: document.getElementById('email').value || null,
    telefone: document.getElementById('telefone').value || null,
    datacontratacao: new Date().toISOString().split('T')[0],
    idsenioridade: Number(document.getElementById('idsenioridade').value)
    // Number(...) converte o texto do <select> em número
    // o backend espera idsenioridade como int, não como texto
  }

  const idTatuador = formTatuador.dataset.idTatuador

  if (idTatuador) {
    await fetch(`${API}/tatuadores/${idTatuador}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(tatuador)
    })
  } else {
    await fetch(`${API}/tatuadores`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(tatuador)
    })
  }

  limparFormulario()
  listarTatuadores()
})

// ─── Abre os dados do tatuador no formulário para edição ───
function preencherFormularioEdicao(tatuador) {
  document.getElementById('nometatuador').value = tatuador.nometatuador
  document.getElementById('cpf').value = tatuador.cpf
  document.getElementById('email').value = tatuador.email || ''
  document.getElementById('telefone').value = tatuador.telefone || ''
  document.getElementById('idsenioridade').value = tatuador.idsenioridade
  // o navegador encontra a <option> com esse value e a seleciona sozinho

  formTatuador.dataset.idTatuador = tatuador.idtatuador

  botaoSubmit.textContent = 'Salvar alteração'
  botaoSubmit.classList.remove('btn-primary')
  botaoSubmit.classList.add('btn-success')
}

// ─── Exclui um tatuador ───
async function deletarTatuador(id) {
  if (!confirm('Tem certeza que deseja excluir este tatuador?')) return

  await fetch(`${API}/tatuadores/${id}`, { method: 'DELETE' })
  listarTatuadores()
}