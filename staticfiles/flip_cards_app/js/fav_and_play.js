function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // проверяем, соответствует ли имя куки
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Ждем полной загрузки DOM перед выполнением скрипта
$(document).ready(function() {
    // Добавляем обработчик клика на все элементы с классом favorites-button
    $('.favorites-button1').on('click', function(event) {
        // Отменяем стандартное поведение браузера при клике
        event.preventDefault();
        
        // Получаем ID слова из data-атрибута кнопки
        var wordId = $(this).data('word-id');
        // Сохраняем ссылку на текущую кнопку
        var $button = $(this);

        // Получаем CSRF-токен из cookies для защиты от CSRF-атак
        var csrftoken = getCookie('csrftoken');

        // Отправляем AJAX-запрос на сервер
        $.ajax({
            // Формируем URL для запроса
            url: '/words/favorite/' + wordId,
            // Указываем метод запроса
            type: 'POST',
            // Добавляем CSRF-токен в заголовки запроса
            headers: {'X-CSRFToken': csrftoken},
            // Обработчик успешного выполнения запроса
            success: function(response) {
                // Если слово добавлено в избранное
                if (response.is_favorite) {
                    // Добавляем класс favorited кнопке
                    $button.addClass('favorited');
                    // Выводим сообщение в консоль
                    console.log('Карточка добавлена в избранное');
                } else {
                    // Удаляем класс favorited с кнопки
                    $button.removeClass('favorited');
                    // Выводим сообщение в консоль
                    console.log('Карточка удалена из избранного');
                }
            },
            // Обработчик ошибки запроса
            error: function() {
                // Выводим сообщение об ошибке в консоль
                console.log('Ошибка при обновлении статуса избранного');
            }
        });
        // Предотвращаем дальнейшее всплытие события
        return false;
    });
});


$(document).ready(function () {
    toastr.options.closeButton = false;
    toastr.options.debug = false;
    toastr.options.newestOnTop = false;
    toastr.options.progressBar = false;
    toastr.options.positionClass = 'toast-top-center';
    toastr.options.preventDuplicates = false;
    toastr.options.onclick = null;
    toastr.options.showDuration = '300';
    toastr.options.hideDuration = '1000';
    toastr.options.timeOut = '5000';
    toastr.options.extendedTimeOut = '1000';
    toastr.options.showEasing = 'swing';
    toastr.options.hideEasing = 'linear';
    toastr.options.showMethod = 'fadeIn';
    toastr.options.hideMethod = 'fadeOut';
    // Обработчик события клика на кнопке воспроизведения аудио
    $('.play-audio-button').on('click', function(event) {
        event.preventDefault(); // предотвратить перезагрузку страницы
        
        var word = $(this).data('word');

        // Получение токена CSRF из элемента meta с именем csrf-token
        var csrftoken = getCookie('csrftoken');

        // AJAX-запрос для получения ссылки на аудио
        $.ajax({
            url: '/words/speak/' + word,
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.audio_url) {
                    var audio = new Audio(response.audio_url);
                    audio.play();
                } else {
                    console.log('Ошибка при получении ссылки на аудио');
                    toastr.error('К сожаления, такого звукового файла пока нет')
                }
            },
            error: function () {
                console.log('Ошибка при запросе ссылки на аудио');
                toastr.error('К сожаления, такого звукового файла пока нет')
            }
        });
    });
});


$(document).ready(function() {
    $('.learned-btn').on('click', function(event) {
        event.preventDefault(); // предотвратить перезагрузку страницы

        var wordId = $(this).data('word-id');
        var isLearned = true;

        // Получение токена CSRF из элемента meta с именем csrf-token
        var csrftoken = getCookie('csrftoken');
        // AJAX-запрос для обновления данных в базе данных 
        $.ajax({
            url: '/words/learned_words/' + wordId,
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            data: {
                word_id: wordId,
                is_learned: true,
            },
            success: function(response) {
                // Обработка успешного ответа здесь
                window.location.reload();
            },
            error: function(xhr, status, error) {
                // Обработка ошибки здесь
            }
        });
    });
});
