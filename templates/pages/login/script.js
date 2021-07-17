const $error = document.querySelector('#error')
const $email = document.querySelector('#email')
const $password = document.querySelector('#password')
const $send = document.querySelector('#send')

$send.addEventListener('click', async () => {
  let data = {
    email: $email.value,
    password: $password.value
  }

  let response = await fetch('/login/', {
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
  if(result == 404) {
    $error.innerText = 'User with this data cannot be found'
  }
})