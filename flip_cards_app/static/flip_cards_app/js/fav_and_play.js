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

$(document).ready(function() {
    // Обработчик события клика на элементе с классом "favorites-button"
    $('.favorites-button').on('click', function(event) {
        event.preventDefault(); // предотвратить перезагрузку страницы
        
        var wordId = $(this).data('word-id');

        // Получение токена CSRF из элемента meta с именем csrf-token
        var csrftoken = getCookie('csrftoken');

        // AJAX-запрос
        $.ajax({
            url: '/words/favorite/' + wordId,
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.is_favorite) {
                    $(this).addClass('favorited');
                    console.log('Карточка добавлена в избранное');
                } else {
                    $(this).removeClass('favorited');
                    console.log('Карточка удалена из избранного');
                }
                window.location.reload();
            }.bind(this), // привязка контекста this к текущему элементу
            error: function() {
                console.log('Ошибка при обновлении статуса избранного');
            }
        });
        return false
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