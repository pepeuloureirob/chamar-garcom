const restaurante = window.RESTAURANTE;
let mesasAtivas = {};
let alertasLiberados = false;

// Ativa som (necessário por regra do navegador)
function ativarAlertas() {
  alertasLiberados = true;
  const audio = document.getElementById("somAlerta");
  audio.play().then(() => audio.pause()).catch(() => {});
  alert("Alertas sonoros ativados 🔔");
}

// Toca som + vibra
function tocarAlerta() {
  if (!alertasLiberados) return;

  const audio = document.getElementById("somAlerta");
  audio.currentTime = 0;
  audio.play().c
