function carregar(restaurante){
  setInterval(()=>{
    fetch(`/status/${restaurante}`)
      .then(r=>r.json())
      .then(d=>{
        let html=""
        for (let m in d){
          html+=`<button onclick="atender('${m}')">Mesa ${m}</button>`
        }
        document.getElementById("mesas").innerHTML = html || "Nenhum chamado"
      })
  },3000)
}

function atender(mesa){
  fetch("/atender",{
    method:"POST",
    headers:{"Content-Type":"application/x-www-form-urlencoded"},
    body:"restaurante="+restaurante+"&mesa="+mesa
  })
}

