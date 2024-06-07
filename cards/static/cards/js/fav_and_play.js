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
    // Обработчик события клика на элементе с классом "favourites-button"
    $('.favourites-button').on('click', function(event) {
        event.preventDefault(); // предотвратить перезагрузку страницы
        
        var cardId = $(this).data('card-id');

        // Получение токена CSRF из элемента meta с именем csrf-token
        var csrftoken = getCookie('csrftoken');

        // AJAX-запрос
        $.ajax({
            url: '/cards/favorite/' + cardId,
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.is_favourite) {
                    $(this).addClass('favourited');
                    console.log('Карточка добавлена в избранное');
                } else {
                    $(this).removeClass('favourited');
                    console.log('Карточка удалена из избранного');
                }
                window.location.reload();
            }.bind(this), // привязка контекста this к текущему элементу
            error: function() {
                console.log('Ошибка при обновлении статуса избранного');
            }
        });
    });
});



$(document).ready(function () {
    toastr.options.closeButton = false;
    toastr.options.debug = false;
    toastr.options.newestOnTop = false;
    toastr.options.progressBar = false;
    toastr.options.positionClass = 'toast-top-right';
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
            url: '/cards/speak/' + word,
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
