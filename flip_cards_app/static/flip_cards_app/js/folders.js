document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Обработка выбора папки
    document.querySelectorAll('.folder-select').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const folderId = this.dataset.folderId;
            const wordId = this.dataset.wordId;
            const button = this.closest('.dropdown').querySelector('button');
            
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
                    // Обновляем иконку и бейдж
                    if (folderId) {
                        button.innerHTML = `
                            <i class="bi bi-folder-fill" style="color:#68539E"></i>
                            <span class="badge bg-secondary">${this.textContent.trim()}</span>
                        `;
                    } else {
                        button.innerHTML = `<i class="bi bi-folder" style="color:#68539E"></i>`;
                    }
                    
                    // Обновляем активный класс
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
            const button = this.closest('.dropdown').querySelector('button');

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
                        // Добавляем слово в новую папку
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
                            <i class="bi bi-folder-fill" style="color:#68539E"></i>
                            <span class="badge bg-secondary">${folderName}</span>
                        `;
                        location.reload();
                    }
                });
            }
        });
    });
});