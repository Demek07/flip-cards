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

   // Обработчик создания папки через calert
    document.querySelectorAll('.new-folder-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const wordId = this.closest('.dropdown').querySelector('.folder-select').dataset.wordId;
            const button = this.closest('.dropdown').querySelector('.favorites-folder');

            calert({
                confirmButton: { innerText: 'Создать', style: { background: '#68539E' } },
                cancelButton: 'Отмена',
                title: 'Новая папка',
                text: 'Введите название папки:',
                icon: 'info',
                inputs: {
                    folderName: {
                        type: 'text',
                        placeholder: 'Название папки'
                    }
                }
            }).then(value => {
                if (value.inputs.folderName) {
                    const folderName = value.inputs.folderName;
                    
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
                            
                            const dropdownMenu = button.closest('.dropdown').querySelector('.dropdown-menu');
                            const newOption = document.createElement('li');
                            newOption.innerHTML = `
                                <a class="dropdown-item folder-select" 
                                   data-folder-id="${data.id}" 
                                   data-word-id="${wordId}" 
                                   href="#">${folderName}</a>
                            `;
                            // Находим разделитель и вставляем новую папку перед ним
                            const separator = dropdownMenu.querySelector('.dropdown-divider').closest('li');
                            // Вставляем новую папку перед разделителем
                            dropdownMenu.insertBefore(newOption, separator);
                            
                            //calert('Папка успешно создана');
                        }
                    });
                }
            });
        });
    });
});