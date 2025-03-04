$(document).ready(function() {
    const csrfToken = getCookie('csrftoken');

    // Обработка выбора папки
    document.querySelectorAll('.folder-select').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const folderId = this.dataset.folderId;
            const wordId = this.dataset.wordId;
            const button = this.closest('.dropdown').querySelector('.favorites-folder');
           
            fetch('/words/catalog/folders/add/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    folder_id: folderId,
                    word_id: wordId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    if (folderId) {
                        button.innerHTML = `
                            <i class="bi bi-folder-fill ms-2 h5" style="color:#68539E"></i>
                            <span class="badge badge-primary">${this.textContent.trim()}</span>
                        `;
                    } else {
                        button.innerHTML = `<i class="bi bi-folder ms-2 h5" style="color:#68539E"></i>`;
                    }
                   
                    this.closest('.dropdown-menu').querySelectorAll('.folder-select').forEach(link => {
                        link.classList.remove('active');
                    });
                    this.classList.add('active');
                }
            });
        });
    });

    // Обработка создания новой папки
    document.querySelectorAll('.new-folder-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const folderName = prompt('Введите название папки:');
            const wordId = this.closest('.dropdown').querySelector('.folder-select').dataset.wordId;
            const button = this.closest('.dropdown').querySelector('.favorites-folder');

            if (folderName) {
                fetch('/words/catalog/folders/create/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        name: folderName
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if(data.id) {
                        return fetch('/words/catalog/folders/add/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrfToken
                            },
                            body: JSON.stringify({
                                folder_id: data.id,
                                word_id: wordId
                            })
                        });
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        button.innerHTML = `
                            <i class="bi bi-folder-fill ms-2 h5" style="color:#68539E"></i>
                            <span class="badge badge-primary">${folderName}</span>
                        `;
                        location.reload();
                    }
                });
            }
        });
    });
});