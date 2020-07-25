const API_URL = (window.location.hostname.indexOf('localhost') >= 0 ) ? 'http://localhost/dreadnought/' : 'http://mandarin.nl/dreadnought/'
const ITEM_ID = document.querySelector("#id").value
const CHAPTER_ID = document.querySelector('#hoofdstuk').value

/*
fetch(`${API_URL}testput`, { method:'PUT'})
  .then( e => e.text() )
  .then ( e => console.log(e) ) 
*/

// https://stackoverflow.com/questions/40893537/fetch-set-cookies-and-csrf
const xsrfCookie = document.cookie.split(';')
    .map(c => c.trim())
    .filter(c => c.startsWith('csrf_access_token='))
    .map ( e=> decodeURIComponent(e.split('=')[1]) )[0] 
const headers = { 'Content-Type':'application/json','X-CSRF-TOKEN': xsrfCookie }

var NEXT_ITEM = 0
fetch(`${API_URL}next_item/${CHAPTER_ID}/${ITEM_ID}`, {
    method:'GET',
    headers,
    credentials:'include'
  })
  .then ( resp => (resp.status==200) ? resp.json() : 0 )
  .then ( e => {
      if (e != 0) NEXT_ITEM = e.id
      else document.querySelector("#save_and_next").disabled = true
  }) 
  .catch( error => console.error(error) )


function serialize() {
  let inputels = document.querySelectorAll("input")
  let textels = document.querySelectorAll("textarea")
  var res = {}
  inputels.forEach ( el => res[el.name] = el.value )
  textels.forEach ( el => res[el.name] = el.value )

  return JSON.stringify(res)
}

function get_retour(action) {
    let rv = ''
    switch(action) {
        case 'stay': rv=`/dreadnought/edit/${ITEM_ID}`; break 
        case 'back': rv=`/dreadnought/${CHAPTER_ID}#${ITEM_ID}`; break 
        case 'next':  rv=`/dreadnought/edit/${NEXT_ITEM}`; break 
    }
    return rv
}

var retour = null
var buttons = document.querySelectorAll(".navigation")
buttons.forEach( el => el.addEventListener('click', e => { 
  let data = serialize()
  retour = get_retour(e.target.attributes.action.value)
  fetch(`${API_URL}edit/${ITEM_ID}`, {
    method: 'PUT', 
    headers,
    credentials:'include',
    body: data,
  })
  .then( _ => document.location = retour )
.catch(err => console.error(err) ) 
}))