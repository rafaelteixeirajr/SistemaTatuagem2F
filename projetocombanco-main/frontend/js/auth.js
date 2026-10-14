// ============================================================
// js/auth.js — Funções compartilhadas de autenticação
// Descrição: Usadas por toda tela protegida, pra checar login
//            e mandar o token em toda requisição pra API.
// ============================================================

// ─── Bloqueia a página se não tiver um token guardado ───
function protegerPagina() {
  const token = localStorage.getItem('token')
  if (!token) {
    window.location.href = 'login.html'
  }
}

// ─── Faz um fetch normal, mas já anexando o token no cabeçalho ───
async function fetchAutenticado(url, opcoes = {}) {
  const token = localStorage.getItem('token')

  opcoes.headers = {
    ...opcoes.headers,           // mantém qualquer header que a chamada já tivesse (tipo Content-Type)
    'Authorization': `Bearer ${token}`
  }

  const resposta = await fetch(url, opcoes)

  if (resposta.status === 401) {
    // o token não é mais válido (expirou, ou foi removido) — manda de volta pro login
    localStorage.removeItem('token')
    window.location.href = 'login.html'
  }

  return resposta
}

// ─── Desloga: apaga o token e volta pra tela de login ───
function sair() {
  localStorage.removeItem('token')
  window.location.href = 'login.html'
}