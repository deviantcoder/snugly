;(
    function() {
        const toastEl = document.getElementById('toast')
        const toastBody = document.getElementById('toast-body')

        const toast = new bootstrap.Toast(toastEl)

        htmx.on('showMessage', (e) => {
            const { text, type } = e.detail

            toastEl.classList.remove('bg-success', 'bg-danger', 'bg-warning', 'bg-info')

            if (type) {
                toastEl.classList.add(`bg-${type}`, 'text-white')
            }    

            toastBody.innerText = text
            toast.show()
        })
    }
)()