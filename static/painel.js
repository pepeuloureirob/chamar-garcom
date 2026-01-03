function carregar(){
  fetch(`/status/${REST}`)
    .then(r=>r.json())
    .then(d=>{
      const div = document.getElementById("mesas");
      div.innerHTML = "";
      for(let i=1;i<=TOTAL;i++){
        const ativo = d.mesas[i];
        const b = document.createElement("button");
        b.innerText = "Mesa " + i;
        b.className = "mesa-btn " + (ativo ? "ativa":"");
        b.onclick = ()=>atender(i);
        div.appendChild(b);
      }
    })
}
function atender(m){
  fetch("/atender",{
    method:"POST",
    headers:{"Content-Type":"application/x-www-form-urlencoded"},
    body:`restaurante=${REST}&mesa=${m}`
  }).then(carregar)
}
setInterval(carregar, 5000);
carregar();

