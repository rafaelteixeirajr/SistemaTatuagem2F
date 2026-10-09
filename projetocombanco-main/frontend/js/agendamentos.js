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

async function listarAgendamentos() {
  const resposta = await fetch(`${API}/agendamentos`)
  const agendamentos = await resposta.json()

  const corpo = document.getElementById('corpo-tabela')
  corpo.innerHTML = ''

  agendamentos.forEach(a => {
    // se existir um desenho salvo, monta uma miniatura; senão, mostra "-"
    const imagemHtml = a.desenhoaprovado
      ? `<img src="${API}/uploads/${a.desenhoaprovado}" style="max-width: 60px; max-height: 60px;">`
      : '-'

    corpo.innerHTML += `
      <tr>
        <td>${a.idagendamento}</td>
        <td>${a.cliente}</td>
        <td>${a.tatuador}</td>
        <td>${a.dataagendamento}</td>
        <td>${a.horaagendamento}</td>
        <td>${a.valortatuagem ?? '-'}</td>
        <td>${a.status}</td>
        <td>${imagemHtml}</td>
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

  const idAgendamento = formAgendamento.dataset.idAgendamento
  let idParaUpload = idAgendamento   // qual id vamos usar pra anexar a imagem, se houver uma

  if (idAgendamento) {
    await fetch(`${API}/agendamentos/${idAgendamento}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(agendamento)
    })
  } else {
    const resposta = await fetch(`${API}/agendamentos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(agendamento)
    })
    const dados = await resposta.json()
    idParaUpload = dados.idagendamento   // pega o id que acabou de ser criado
  }

  // ─── Se um arquivo foi escolhido, envia numa segunda chamada, separada ───
  const arquivo = document.getElementById('desenho').files[0]
  if (arquivo) {
    const formData = new FormData()   // FormData, não JSON — porque tem um arquivo dentro
    formData.append('arquivo', arquivo)   // "arquivo" precisa ser o mesmo nome do parâmetro no FastAPI

    await fetch(`${API}/agendamentos/${idParaUpload}/desenho`, {
      method: 'POST',
      body: formData
      // repare que aqui NÃO colocamos o header Content-Type — o navegador
      // define esse cabeçalho sozinho quando o corpo é um FormData
    })
  }

  limparFormulario()
  listarAgendamentos()
})