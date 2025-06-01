function fetchAndRenderNotes() {
  fetch('/api/notes')
    .then((response) => response.json())
    .then((notes) => {
      const container = document.getElementById('notes')
      container.innerHTML = '' // Vide le conteneur avant de recharger

      notes.forEach((note) => {
        const div = document.createElement('div')
        div.className = 'note'

        const h2 = document.createElement('h2')
        h2.textContent = note.title

        const p = document.createElement('p')
        p.textContent = note.content

        const form = document.createElement('form')
        const label = document.createElement('label')
        label.htmlFor = `note-${note.id}`
        label.textContent = 'done'

        const checkbox = document.createElement('input')
        checkbox.type = 'checkbox'
        checkbox.id = `note-${note.id}`
        checkbox.checked = note.done
        checkbox.dataset.id = note.id

        checkbox.addEventListener('change', () => {
          fetch(`/api/notes/${note.id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ done: checkbox.checked })
          }).then(response => response.json())
        })

        const deleteButton = document.createElement('button')
        deleteButton.textContent = 'Supprimer'
        deleteButton.addEventListener('click', (event) => {
          event.preventDefault()
          fetch(`/api/notes/${note.id}`, {
            method: 'DELETE'
          }).then(response => response.json())
        })

        form.appendChild(label)
        form.appendChild(checkbox)

        div.appendChild(h2)
        div.appendChild(p)
        div.appendChild(form)
        div.appendChild(deleteButton)

        container.appendChild(div)
      })
    })
}

document.addEventListener('DOMContentLoaded', () => {
  fetchAndRenderNotes()

  const socket = io()
  socket.on('note_updated', () => {
    fetchAndRenderNotes()
  })
})
