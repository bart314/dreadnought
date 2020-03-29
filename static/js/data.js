const months = ['Jan','Feb','March','April','May','June','July','Aug','Sept','Oct','Nov','Dec']

const xhttp = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP"); 
xhttp.onreadystatechange = function() {
    if (this.readyState ==4  && this.status==200) { 
      JSON.parse(this.response).forEach( (el) => { 
        let d = new Date(el.jaar +'-' + el.datum) 
        let d_full = `${months[d.getUTCMonth()]} ${d.getDate()}`
        let item = document.importNode(
            document.querySelector("#item").content.querySelector("div"), true)
        let link = document.importNode(document.querySelector("#item-link").content, true)
        let footer = document.importNode(document.querySelector("#item-footer").content, true) 

        link.querySelector('a').setAttribute('href', `#${el.id}`) 

        footer.querySelector('p.ref').textContent = `Dreadnought, p.${el.paginanummer}`
        if (localStorage.getItem('dn-token')) {
          footer.querySelector('a.edit').setAttribute('href', `edit/${el.id}`)
          footer.querySelector('a.delete').setAttribute('href', `del/${el.id}`) 
        }

        item.querySelector('time').setAttribute("datetime", d)
        item.querySelector('time').setAttribute('id', el.id)
        item.querySelector('span.jaar').textContent = el.jaar
        item.querySelector('span.datum').textContent = d_full 

        item.querySelector('h2').textContent = el.koptekst
        item.querySelector('h2').appendChild(link)
        item.querySelector('p').innerHTML = el.broodtekst
        item.querySelector('p').appendChild(footer)

        let li = document.createElement('li')
        li.appendChild(item) 
        document.querySelector('#timeline').appendChild(li)
      })
    }
}
xhttp.open("GET", "http://localhost/dreadnought/timeline/39")
xhttp.send()

if (localStorage.getItem('dn-login')) {
  console.log('CHECK')
  document.querySelector("#login-button").innerHTML = 'Ingelogd!' 
}

function show_anchor(el) {
    el.firstElementChild.classList.add('active')
}
function hide_anchor(el) {
    el.firstElementChild.classList.remove('active')
}




