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
    $('.play-audio-button').on('click', function (event) {
        event.preventDefault();
        
        var word = $(this).data('word');
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: '/words/speak/' + word,
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            success: function (response) {
                if (response.audio_url) {
                    const audio = new Audio();
                    audio.preload = 'auto';
                    audio.src = response.audio_url;
                    
                    setTimeout(() => {
                        audio.currentTime = 0;
                        audio.play();
                    }, 100);
                    
                } else {
                    toastr.error('К сожаления, такого звукового файла пока нет')
                }
            },
            error: function () {
                toastr.error('К сожаления, такого звукового файла пока нет')
            }
        });
    });
    $(document).on('click', '.learned-btn', function (e) {
        e.preventDefault();
        const wordId = $(this).data('word-id');
        const button = $(this);
        const card = button.closest('.card'); // находим родительскую карточку
        const isFlipPage = window.location.pathname.includes('flip');
        
        $.ajax({
            url: `/words/learned_words/${wordId}`,
            type: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            data: {
                word_id: wordId,
                is_learned: true,
            },
            success: function (response) {
                if (response.is_learned) {
                    if (isFlipPage) {
                        card.fadeOut(400, function() {
                            card.remove();
                        });
                    } else {
                        button.html('<i class="bi bi-patch-check-fill ms-2 h5" style="color:#68539E"></i>');
                        button.addClass('learned');
                    }
                } else {
                    button.html('<i class="bi bi-patch-check ms-2 h5" style="color:#68539E"></i>');
                    button.removeClass('learned');
                }
            },

            error: function () {
                console.log('Ошибка при обновлении статуса слова');
            }
        });
        return false;
    });
        // Добавляем HTML кнопки в body
    $('body').append('<button id="scrollTopBtn" class="scroll-top-btn"><i class="bi bi-chevron-double-up"></i></button>');

    // Показываем/скрываем кнопку при скролле
    $(window).scroll(function() {
        if ($(this).scrollTop() > 200) {
            $('#scrollTopBtn').fadeIn();
        } else {
            $('#scrollTopBtn').fadeOut();
        }
    });

    // Обработчик клика - плавная прокрутка вверх
    $('#scrollTopBtn').click(function() {
        $('html, body').animate({scrollTop: 0}, 800);
        return false;
    });
});
