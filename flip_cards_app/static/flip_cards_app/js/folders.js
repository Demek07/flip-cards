$(document).ready(function() {
    const csrfToken = getCookie('csrftoken');

    // Обработка выбора папки
    $(document).on('click', '.folder-select', function(e) {
        e.preventDefault();
        const folderId = $(this).data('folder-id');
        const wordId = $(this).data('word-id');
        const button = $(this).closest('.dropdown').find('.favorites-btn');
        
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
            if (data.is_favorite) {
                button.html('<i class="bi bi-heart-fill" style="color:#68539E"></i>');
                // Заменяем заголовок "Добавить в избранное" на кнопку удаления
                const dropdownMenu = $(this).closest('.dropdown-menu');
                dropdownMenu.find('.dropdown-header').closest('li').replaceWith(`
                    <li>
                        <a class="dropdown-item remove-favorite" href="#" data-word-id="${wordId}">
                            <i class="bi bi-x-circle"></i> Убрать из избранного
                        </a>
                    </li>
                `);
                $(this).closest('.dropdown-menu').find('.folder-select').removeClass('active');
                $(this).addClass('active');
            }
        });
    });

    // Обработчик создания папки
    $(document).on('click', '.new-folder-btn', function(e) {
        e.preventDefault();
        const wordId = $(this).closest('.dropdown').find('.folder-select').data('word-id');
        const button = $(this).closest('.dropdown').find('.favorites-btn');

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
                        button.html('<i class="bi bi-heart-fill" style="color:#68539E"></i>');
                        
                        const newOption = `
                            <li>
                                <a class="dropdown-item folder-select" 
                                   data-folder-id="${data.id}" 
                                   data-word-id="${wordId}" 
                                   href="#">${folderName}</a>
                            </li>`;
                        $(this).closest('.dropdown-menu').find('.dropdown-divider').closest('li').before(newOption);
                    }
                });
            }
        });
    });
    // Обработка удаления из избранного
    $(document).on('click', '.remove-favorite', function(e) {
        e.preventDefault();
        const wordId = $(this).data('word-id');
        const folderId = $(this).closest('.dropdown-menu').find('.folder-select.active').data('folder-id');
        const button = $(this).closest('.dropdown').find('.favorites-btn');
        
        $.ajax({
            url: `/words/favorite/${folderId}/${wordId}`,
            type: 'POST',
            headers: {'X-CSRFToken': csrfToken},
            success: function(response) {
                if (!response.is_favorite) {
                    button.html('<i class="bi bi-heart" style="color:#68539E"></i>');
                    // Заменяем пункт "Удалить из избранного" на заголовок "Добавить в избранное"
                    const dropdownMenu = button.closest('.dropdown').find('.dropdown-menu');
                    dropdownMenu.find('.remove-favorite').closest('li').replaceWith(`
                        <li>
                            <h6 class="dropdown-header">Добавить в избранное</h6>
                        </li>
                    `);
                    // Снимаем активное состояние со всех пунктов меню
                    dropdownMenu.find('.folder-select').removeClass('active');
            }
        },
            error: function() {
                console.log('Ошибка при удалении из избранного1');
            }
        });
        return false;
    });
});

