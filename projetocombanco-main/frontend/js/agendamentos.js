// endereço da nossa API backend
const API = 'http://127.0.0.1:8000'

// elementos do formulário e do botão de enviar
const formAgendamento = document.getElementById('form-agendamento')
const botaoSubmit = document.getElementById('btn-submit-agendamento')
const blocoStatus = document.getElementById('bloco-status')

// limpa o formulário e devolve para o modo de cadastro
function limparFormulario() {
  formAgendamento.reset()
  delete formAgendamento.dataset.idAgendamento
  botaoSubmit.textContent = 'Cadastrar'
  botaoSubmit.classList.remove('btn-success')
  botaoSubmit.classList.add('btn-primary')
  blocoStatus.style.display = 'none'   // esconde o status de novo — cadastro não usa esse campo
}

// ─── Busca os clientes na API e preenche o <select> ───
async function carregarClientes() {
  const resposta = await fetch(`${API}/clientes`)
  const clientes = await resposta.json()

  const select = document.getElementById('idcliente')
  select.innerHTML = '<option value="">Cliente...</option>'

  clientes.forEach(c => {
    select.innerHTML += `<option value="${c.idcliente}">${c.nome}</option>`
  })
}

// ─── Busca os tatuadores na API e preenche o <select> ───
async function carregarTatuadores() {
  const resposta = await fetch(`${API}/tatuadores`)
  const tatuadores = await resposta.json()

  const select = document.getElementById('idtatuador')
  select.innerHTML = '<option value="">Tatuador...</option>'

  tatuadores.forEach(t => {
    select.innerHTML += `<option value="${t.idtatuador}">${t.nometatuador}</option>`
  })
}

carregarClientes()
carregarTatuadores()

// ─── Carrega a lista de agendamentos ao abrir a página ───
async function listarAgendamentos() {
  const resposta = await fetch(`${API}/agendamentos`)
  const agendamentos = await resposta.json()

  const corpo = document.getElementById('corpo-tabela')
  corpo.innerHTML = ''

  agendamentos.forEach(a => {
    corpo.innerHTML += `
      <tr>
        <td>${a.idagendamento}</td>
        <td>${a.cliente}</td>
        <td>${a.tatuador}</td>
        <td>${a.dataagendamento}</td>
        <td>${a.horaagendamento}</td>
        <td>${a.valortatuagem ?? '-'}</td>
        <td>${a.status}</td>
        <td>
          <button class="btn btn-sm btn-warning me-2" onclick='preencherFormularioEdicao(${JSON.stringify(a)})'>Editar</button>
          <button class="btn btn-sm btn-danger" onclick="deletarAgendamento(${a.idagendamento})">Excluir</button>
        </td>
      </tr>`
  })
}

listarAgendamentos()

// ─── Cadastrar e atualizar agendamentos ───
formAgendamento.addEventListener('submit', async (e) => {
  e.preventDefault()

  const agendamento = {
    idcliente: Number(document.getElementById('idcliente').value),
    idtatuador: Number(document.getElementById('idtatuador').value),
    dataagendamento: document.getElementById('dataagendamento').value,
    horaagendamento: document.getElementById('horaagendamento').value,
    descricaotatuagem: document.getElementById('descricaotatuagem').value || null,
    valortatuagem: document.getElementById('valortatuagem').value
      ? Number(document.getElementById('valortatuagem').value)
      : null,
    status: document.getElementById('status').value
  }
  // no cadastro, o campo status vai vazio dentro do JSON — sem problema,
  // porque o INSERT no backend nem usa esse valor (o banco aplica 'pendente' sozinho)

  const idAgendamento = formAgendamento.dataset.idAgendamento

  if (idAgendamento) {
    await fetch(`${API}/agendamentos/${idAgendamento}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(agendamento)
    })
  } else {
    await fetch(`${API}/agendamentos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(agendamento)
    })
  }

  limparFormulario()
  listarAgendamentos()
})

// ─── Abre os dados do agendamento no formulário para edição ───
function preencherFormularioEdicao(agendamento) {
  document.getElementById('idcliente').value = agendamento.idcliente
  document.getElementById('idtatuador').value = agendamento.idtatuador
  document.getElementById('dataagendamento').value = agendamento.dataagendamento
  document.getElementById('horaagendamento').value = agendamento.horaagendamento
  document.getElementById('descricaotatuagem').value = agendamento.descricaotatuagem || ''
  document.getElementById('valortatuagem').value = agendamento.valortatuagem || ''

  document.getElementById('status').value = agendamento.status
  blocoStatus.style.display = 'block'   // só na edição o campo de status aparece

  formAgendamento.dataset.idAgendamento = agendamento.idagendamento

  botaoSubmit.textContent = 'Salvar alteração'
  botaoSubmit.classList.remove('btn-primary')
  botaoSubmit.classList.add('btn-success')
}

// ─── Exclui um agendamento ───
async function deletarAgendamento(id) {
  if (!confirm('Tem certeza que deseja excluir este agendamento?')) return

  await fetch(`${API}/agendamentos/${id}`, { method: 'DELETE' })
  listarAgendamentos()
}