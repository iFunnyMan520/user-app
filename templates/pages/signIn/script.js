const $error = document.querySelector('#error')
const $first_name = document.querySelector('#first-name')
const $last_name = document.querySelector('#last-name')
const $email = document.querySelector('#email')
const $password = document.querySelector('#password')
const $superadmin = document.querySelector('#superadmin')
const $send = document.querySelector('#send')

$send.addEventListener('click', async () => {
  let data = {
    first_name: $first_name.value,
    last_name: $last_name.value,
    email: $email.value,
    password: $password.value,
    superuser: $superadmin.checked
  }

  let response = await fetch('/signIn/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    },
    body: JSON.stringify(data)
  })



  let result = await response.status

  if(result == 200) {
    window.location.replace('/')
  }
  if(result == 403) {
    $error.innerText = 'User already exist'
  }
})