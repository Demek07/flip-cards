// $(document).ready(function() {
//     // Обработчик события клика на элементе с классом "favourites-button"
//     $('.favourites-button').on('click', function(event) {
//         event.preventDefault(); // предотвратить перезагрузку страницы
        
//         var cardId = $(this).data('card-id');
//         console.log(cardId);

//         // AJAX-запрос
//         $.ajax({
//             url: '/cards/favorite/' + cardId,
//             type: 'POST',
//             headers: {'X-CSRF-TOKEN': '{{ csrf_token() }}'},
//             success: function(response) {
//                 if (response.is_favourite) {
//                     $(this).addClass('favourited');
//                 } else {
//                     $(this).removeClass('favourited');
//                 }
//             }.bind(this), // привязка контекста this к текущему элементу
//             error: function() {
//                 console.log('Ошибка при обновлении статуса избранного');
//             }
//         });
//     });
// });

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