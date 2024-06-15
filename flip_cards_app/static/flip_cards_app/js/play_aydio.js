$(document).ready(function() {
    // Обработчик события клика на кнопке воспроизведения аудио
    $('.play-audio-button').on('click', function(event) {
        event.preventDefault(); // предотвратить перезагрузку страницы
        
        var word = $(this).data('word');

        // AJAX-запрос для получения ссылки на аудио
        $.ajax({
            url: '{% url 'get_word_audio' %}',
            type: 'POST',
            data: {
                'word': word
            },
            success: function(response) {
                if (response.audio_url) {
                    var audio = new Audio(response.audio_url);
                    audio.play();
                } else {
                    console.log('Ошибка при получении ссылки на аудио');
                }
            },
            error: function() {
                console.log('Ошибка при запросе ссылки на аудио');
            }
        });
    });
});