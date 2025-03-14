$(document).ready(function() {
    const csrfToken = getCookie('csrftoken');

    // Добавляем в начало файла folders.js
    $(document).ready(function() {
        // Добавляем кнопку закрытия к каждому сообщению
        $('.messages li').each(function() {
            $(this).append('<button type="button" class="btn-close float-end" aria-label="Close"></button>');
        });

        // Обработчик клика по кнопке закрытия
        $(document).on('click', '.btn-close', function() {
            $(this).closest('li').fadeOut(300, function() {
                $(this).remove();
                // Если сообщений больше нет, скрываем весь блок
                if ($('.messages li').length === 0) {
                    $('.messages').fadeOut(300);
                }
            });
        });
    });    

    // Обработка выбора папки
    $(document).on('click', '.folder-select', function(e) {
        e.preventDefault();
        const folderId = $(this).data('folder-id');
        const wordId = $(this).data('word-id');
        const button = $(this).closest('.dropdown').find('.favorites-btn');
        
        fetch('/words/favorites/folders/add/', {
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
        const wordId = $(this).closest('.dropdown').find('.favorites-btn').data('word-id');
        const button = $(this).closest('.dropdown').find('.favorites-btn');
        const isFromWordContext = !!wordId; // проверяем, создаётся ли папка из контекста слова

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
                
                fetch('/words/favorites/folders/create/', {
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
                    const folderId = data.id;
                    if (isFromWordContext) {
                        // Если создаём папку из контекста слова, добавляем слово в папку
                        return fetch('/words/favorites/folders/add/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrfToken
                            },
                            body: JSON.stringify({
                                folder_id: folderId,
                                word_id: wordId
                            }),
                        }).then(response => response.json())
                            .then(addData => {
                                return {
                                    data: addData,
                                    folderId: folderId,
                                    folderName: folderName
                                };
                            });
                    } else {
                        // Если создаём папку из контекста папки, перезагружаем страницу
                        location.reload();
                    }
                })
                .then(result => {
                    if (result && result.data.is_favorite) {
                        // Обновляем все выпадающие меню на странице
                        $('.dropdown-menu').each(function() {
                            const currentWordId = $(this).closest('.dropdown').find('.favorites-btn').data('word-id');
                            const currentMenu = $(this);
                            
                            // Добавляем новую папку во все меню
                            const newFolderOption = `
                                <li>
                                    <a class="dropdown-item folder-select"
                                    data-folder-id="${result.folderId}"
                                    data-word-id="${currentWordId}"
                                    href="#">
                                    <i class="bi bi-folder"></i> ${result.folderName}
                                    </a>
                                </li>`;
                                
                            currentMenu.find('.dropdown-divider').closest('li').before(newFolderOption);
                        });
                        
                        // Обновляем текущее меню
                        button.html('<i class="bi bi-heart-fill" style="color:#68539E"></i>');
                        const dropdownMenu = button.closest('.dropdown').find('.dropdown-menu');
                        // Заменяем "Добавить в избранное" на "Убрать из избранного"
                        dropdownMenu.find('.dropdown-header').closest('li').replaceWith(`
                            <li>
                                <a class="dropdown-item remove-favorite" href="#" data-word-id="${wordId}">
                                    <i class="bi bi-x-circle"></i> Убрать из избранного
                                </a>
                            </li>
                        `);                        
                        dropdownMenu.find('.folder-select').removeClass('active');
                        dropdownMenu.find(`[data-folder-id="${result.folderId}"]`).addClass('active');
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
            url: `/words/favorites/${folderId}/${wordId}`,
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
    // Обработчик переименования папки
    $(document).on('click', '.edit-folder', function(e) {
        e.preventDefault();
        const folderId = $(this).data('folder-id');
        const currentName = $(this).closest('.card').find('.card-title').text().trim();
        
        calert({
            confirmButton: { innerText: 'Сохранить', style: { background: '#68539E' } },
            cancelButton: 'Отмена',
            title: 'Переименовать папку',
            text: 'Введите новое название папки:',
            icon: 'info',
            inputs: {
                folderName: {
                    type: 'text',
                    placeholder: 'Название папки',
                    value: currentName
                }
            },
            
        }).then(value => {
            if (value.inputs.folderName) {
                fetch('/words/favorites/folders/rename/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        folder_id: folderId,
                        name: value.inputs.folderName
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        location.reload();
                    }
                });
            }
        });
    });

    // Обработчик удаления папки
    $(document).on('click', '.delete-folder', function(e) {
        e.preventDefault();
        const folderId = $(this).data('folder-id');
        
        calert({
            confirmButton: { innerText: 'Удалить', style: { background: '#dc3545' } },
            cancelButton: 'Отмена',
            title: 'Удалить папку?',
            text: 'Все слова из этой папки будут удалены из избранного',
            icon: 'warning'
        }).then(result => {
            if (result.isConfirmed) {
                fetch('/words/favorites/folders/delete/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        folder_id: folderId
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        location.reload();
                    }
                });
            }
        });
    });
    // Добавляем обработчик для удаления из избранного в превью
    $(document).on('click', '.remove-from-favorite', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        const button = $(this);
        const wordId = button.data('word-id');
        const folderId = button.data('folder-id');
        const wordCard = button.closest('.word-card');
        const wordsCountElement = $('.all_text.words-count');
        const currentPage = window.location.href;
        
        $.ajax({
            url: `/words/favorites/${folderId}/${wordId}`,
            type: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function(response) {
                if (!response.is_favorite) {
                    wordCard.fadeOut(300, function() {
                        $(this).remove();
                        
                        // Обновляем список карточек
                        $.get(currentPage, function(data) {
                            $('.words-container').html($(data).find('.words-container').html());
                        });
                        
                        // Обновляем счётчик слов
                        const currentText = wordsCountElement.text();
                        const currentCount = parseInt(currentText.match(/\d+/)[0]);
                        wordsCountElement.text(`Слов в папке: ${currentCount - 1}`);

                        if ($('.word-card').length === 0) {
                            $('.words-container').html('<p class="text-center">В этой папке пока нет слов</p>');
                        }
                    });
                }
            },
            error: function() {
                console.log('Ошибка при удалении из избранного');
            }
        });
    });
    // Обработчик отправки формы загрузки файла
    $(document).on('submit', '#uploadForm', function (e) {
        // Отменяем стандартное поведение формы
        e.preventDefault();
        
        // создаем объект FormData из текущей формы
        const formData = new FormData(this);
        // получаем элементы прогресс-бара и статуса
        const $progressBar = $('.progress-bar');
        const $progressDiv = $('#uploadProgress');
        const $statusText = $('#uploadStatus');
        
        // Устанавливаем стили для прогресс-бара
        $progressBar.css({
            'background-color': '#68539E', // фирменный цвет
            'color': '#fff',               // цвет текста
            'display': 'flex',             // гибкое позиционирование
            'align-items': 'center',       // центрирование по вертикали
            'justify-content': 'center'    // центрирование по горизонтали
        });
        // Добавляем анимацию прогресс-бара
        $progressBar.addClass('progress-bar-animated progress-bar-striped');
        // показываем контейнер прогресс-бара 
        $progressDiv.show();
        // Устанавливаем начальную ширину прогресс-бара на 0%
        $progressBar.width('0%');
        // Устанавливаем начальный текст статуса
        $progressBar.text('Начинаем загрузку...');

        // Запускаем проверку прогресса каждые 500 мс
        const progressCheck = setInterval(() => {
            $.get(`${window.location.href}progress/`, function(data) {
                const progress = Math.round(data.progress);
                // Добаввляем плавную анимацию прогресс-бара
                $progressBar.css('transition', 'width 0.5s ease-in-out');
                // Обновляем ширину прогресс-бара
                $progressBar.width(progress + '%');
                // Обновляем текст прогресса
                $progressBar.text('Загрузка слов... ' + progress + '%');
                // Если прогресс достиг 100%, останавливаем проверку прогресса
                if(progress >= 100) {
                    clearInterval(progressCheck);
                }
            });
        }, 500);

        // Отправляем AJAX-запрос для загрузки файла
        $.ajax({
            url: window.location.href,
            method: 'POST',
            data: formData,
            processData: false,     // Отключаем обработку данный Query
            contentType: false,     // Отключаем установку заголовка Content-Type
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')  // Добавляем CSRF-токен в заголовок
            },
            success: function (response) {
                // Обрабатываем успешную загрузку файла
                clearInterval(progressCheck);
                $progressBar.removeClass('progress-bar-animated');
                $progressBar.width('100%');
                $progressBar.text('Загрузка успешно завершена!');
                // Перезагружаем страницу через 1 секунду
                setTimeout(() => {
                    $progressDiv.fadeOut(300, function() {
                        window.location.href = window.location.href;
                    });
                }, 1000);
            },
            error: function (xhr) {
                // Обрабатываем ошибку при загрузке файла
                clearInterval(progressCheck);
                $progressBar.removeClass('progress-bar-animated');
                $progressBar.css('background-color', '#dc3545'); // красный цвет
                $progressBar.text('Произошла ошибка при загрузке');
                // Перезагружаем страницу через 1 секунду
                setTimeout(() => {
                    $progressDiv.fadeOut(300, function() {
                        window.location.href = window.location.href;
                    });
                }, 1000);
            }
        });
    });
});

