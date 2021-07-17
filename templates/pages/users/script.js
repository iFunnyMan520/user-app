const $edit_buttons = document.querySelectorAll('.edit')
const $delete_buttons = document.querySelectorAll('.delete')
const $new_user_button = document.querySelector('.new-user')
const $logout_button = document.querySelector('.logout')

const $edit_block = document.querySelector('.edit-block')
const $new_user_block = document.querySelector('.new-user-block')
const $edit_exit = document.querySelector('.edit-fas')
const $new_user_exit = document.querySelector('.new-user-fas')

const $table = document.querySelector('table tbody')
const $tb_title = document.querySelector('th').closest('tr')


function insertAfter(newNode, existingNode) {
  existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
}

$logout_button.addEventListener('click', async () => {
  let response = await fetch('/logout/')

  let result = await response.status

  if (result == 200) {
    window.location.replace('/login/')
  }
})

$edit_exit.addEventListener('click', () => {
  $edit_block.classList.add('non-active')
})

$new_user_exit.addEventListener('click', () => {
  $new_user_block.classList.add('non-active')
})

$new_user_button.addEventListener('click', async () => {
  $new_user_block.classList.remove('non-active')
  const $first_name = $new_user_block.querySelector('#first-name')
  const $last_name = $new_user_block.querySelector('#last-name')
  const $email = $new_user_block.querySelector('#email')
  const $admin = $new_user_block.querySelector('#superadmin')
  const $password = $new_user_block.querySelector('#password')
  const $send = $new_user_block.querySelector('#send')
  const $error = $new_user_block.querySelector('#error')

  $first_name.value = ''
  $last_name.value = ''
  $email.value = ''
  $password.value = ''
  $admin.checked = false
  $error.innerHTML = ''

  $send.addEventListener('click', async () => {
    let data = {
      first_name: $first_name.value,
      last_name: $last_name.value,
      email: $email.value,
      password: $password.value,
      superuser: $admin.checked,
    }

    let response = await fetch('/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8'
      },
      body: JSON.stringify(data)
    })

    let result = await response.status

    if(result == 403) {
      $error.innerText = 'User already exist'
    }

    if(result == 200) {
      let new_user = await response.json()

      const $new_tr = document.createElement('tr')

      $new_tr.id = new_user.id

      $new_tr.innerHTML = `
        <td class='first-name'>${new_user.first_name}</td>
        <td class='last-name'>${new_user.last_name}</td>
        <td class='email'>${new_user.email}</td>
        <td class='admin' style="text-align: center;">
            
        </td>
        {% if current_user.superuser %}
        <td><button class="edit">Edit</button></td>
        <td><button class="delete">Delete</button></td>
        {% else %}
        <td><button disabled class="edit">Edit</button></td>
        <td><button disabled class="delete">Delete</button></td>
        {% endif %}
      `

      if(new_user.superuser){
        const $is_admin = $new_tr.querySelector('.admin')
        $is_admin.innerHTML = '<i class="fas fa-check"></i>'
      }
      
      edit_button_func($new_tr.querySelector('.edit'))
      delete_button_func($new_tr.querySelector('.delete'))
      
      console.log($edit_buttons);

      insertAfter($new_tr, $tb_title)

      $new_user_block.classList.add('non-active')
    }

  })
})

edit_button_func = function(btn) {
  btn.addEventListener('click', async () => {
    let tr = btn.closest('tr')
    $edit_block.classList.remove('non-active')
    const $first_name = $edit_block.querySelector('#first-name')
    const $last_name = $edit_block.querySelector('#last-name')
    const $email = $edit_block.querySelector('#email')
    const $admin = $edit_block.querySelector('#superadmin')
    const $send = $edit_block.querySelector('#send')
    const $error = $edit_block.querySelector('#error')

    $first_name.value = ''
    $last_name.value = ''
    $email.value = ''
    $admin.checked = false
    $error.innerHTML = ''

    $send.addEventListener('click', async () => {
      let data = {
        user_id: tr.id,
        first_name: $first_name.value,
        last_name: $last_name.value,
        email: $email.value,
        superuser: $admin.checked,
      }

      let response = await fetch('/', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(data)
      })

      let result = await response.status

      if(result == 403) {
        $error.innerText = 'User already exist'
      }
      
      if(result == 200) {
        $edit_block.classList.add('non-active')
        let edited_user = await response.json()
        const $new_first_name = tr.querySelector('.first-name')
        const $new_last_name = tr.querySelector('.last-name')
        const $new_email = tr.querySelector('.email')
        const $new_admin = tr.querySelector('.admin')

        $new_first_name.innerHTML = edited_user.first_name
        $new_last_name.innerHTML = edited_user.last_name
        $new_email.innerHTML = edited_user.email
        if(edited_user.superuser) {
          $new_admin.innerHTML = '<i class="fas fa-check"></i>'
        }
      }
    })
  })
}

$edit_buttons.forEach(btn => {
  edit_button_func(btn)
});

delete_button_func = function(btn) {
  btn.addEventListener('click', async () => {
    let tr = btn.closest('tr')
    let data =  {
      user_id: tr.id
    }

    let response = await fetch('/', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json;charset=utf-8'
      },
      body: JSON.stringify(data)
    })

    let result = await response.status

    if(result == 200) {
      tr.remove()
    }
  })
}

$delete_buttons.forEach(btn => {
  delete_button_func(btn)
});