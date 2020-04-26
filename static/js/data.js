const API_BASE = 'http://localhost/dreadnought'
const months = ['Jan','Feb','March','April','May','June','July','Aug','Sept','Oct','Nov','Dec'] 
const xhttp = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP"); 
var user_logged_in = null

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
        if (loggedin()) {
          footer.querySelector('a.edit').setAttribute('href', `${API_BASE}/edit/${el.id}`)
          footer.querySelector('a.delete').setAttribute('href', `${API_BASE}/del/${el.id}`) 
        } else {
          footer.querySelector('p.edit').innerHTML = ''
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
xhttp.open("GET", API_BASE + "/timeline/39")
xhttp.send()

// LOGIN / LOGOUT button
// Ik wilde gebruik maken van een IIFE, maar dat werkt niet lekker met 
// puntkomma's. Daarom maar een named function...
function login_button() {
  const login = loggedin()
  const b = document.querySelector('#login-button') 
  b.innerHTML = login ? 'Logout' : 'Login'
  b.addEventListener('click', (e) => {
    if (loggedin()) logout()
    else document.location = API_BASE + '/login' 
  })
}
login_button()


function logout() { 
  console.log('logout')
  //https://stackoverflow.com/questions/2144386/how-to-delete-a-cookie
  document.cookie = 'csrf_access_token=; Max-Age=-99999'
  user_logged_in = false
  const req = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP"); 
  req.onreadystatechange = function() {
    if (this.readyState ==4  && this.status==200) { 
      document.location = API_BASE
    }
  } 
  req.open("GET", API_BASE + "/logout")
  req.send()
}

function loggedin() {
  // lazy loading om te kijken of user is ingelogd
  if (user_logged_in===null) {
    let str = document.cookie
    user_logged_in = str.indexOf('csrf_access_token')===0 ? true : false
  } 
  return user_logged_in
}

function show_anchor(el) {
    el.firstElementChild.classList.add('active')
}
function hide_anchor(el) {
    el.firstElementChild.classList.remove('active')
}




