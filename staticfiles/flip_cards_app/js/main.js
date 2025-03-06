document.addEventListener("DOMContentLoaded", function () {
    /*игра начало*/
    const remainsElement = document.getElementById("remains");
    let mark = "";
    let left = "";
    let right = "";
    // let remains = 10;
    if (remainsElement) {
        remains = parseInt(remainsElement.innerHTML);
    }
    // let user_id = document.getElementById("user_id").innerHTML.slice(7);
    let id = "";
    let error_count = 0;
    let error_style = `
    background-color: #BF3740;
    border-color : #B9242D;`
    let correct_style = `
    background-color: #73A720;
    border-color : #68961D;`
    let select_style = `
    background-color: #B7ABD8;
    border-color : #B7ABD8;`
    let light_style = `
    background-color: #eae7dc;
    border-color : #CCC;
    color: #666;`
    let dark_style = `
    background-color: #68539E;
    border-color : #68539E;
    color: #FFF;`

    // Функции
    window.save_results = function (word_id, errors, rights) {
        // Отправляем AJAX-запрос на сервер для обновления счетчиков в базе данных
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/words/save_results/',
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            data: {
                word_id: word_id,
                errors: errors,
                rights: rights
            },
            success: function (response) {
                // Обрабатываем ответ сервера, если это необходимо
                console.log(response);
            },
            error: function (xhr, status, error) {
                // Обрабатываем ошибки, которые могут возникнуть во время отправки AJAX-запроса
                console.error(error);
            }
        });
    }

    window.click1 = function (id_word) {
        id = id_word.slice(1);
        if (id_word[0] == "l") {
            left = id_word;
        } else if (id_word[0] == "r") {
            right = id_word;
        }
        if (mark == "") {
            mark = id_word;
        }
        document.getElementById(mark).style = select_style;
        if (left.slice(1) == right.slice(1)) {
            remains = remains - 1;
            save_results(mark.slice(1), 0, 1);
            document.getElementById(left).style = correct_style;
            document.getElementById(right).style = correct_style;
            document.getElementById("remains").innerHTML = remains;
            mark = "";
            left = "";
            right = "";
            setTimeout(function () {
                // console.log(id);
                // console.log(user_id);
                remove(id);
            }, 333);
            if ((remains == 0) & (error_count == 0)) {
                calert({
                    confirmButton: { innerText: 'Да', style: { background: '#68539E' } },
                    cancelButton: 'Нет',
                    title: "Поздравляем!",
                    text: { innerHTML: 'Вы без ошибок определили все пары! Желаете сыграть еще раз?' },
                    icon: 'success'
                }).then((result) => {
                    if (result.isConfirmed) { location.reload(true); }
                });

                // if (confirm('Вы без ошибок определили все пары! Желаете повторить?')) {
                //     location.reload();}
            } else if ((remains == 0) & (error_count != 0)) {
                calert({
                    confirmButton: { innerText: 'Да', style: { background: '#68539E' } },
                    cancelButton: 'Нет',
                    // title: "Поздравляем!",
                    text: { innerHTML: 'Вы ошиблись ' + error_count + ' раз(а). Желаете повторить?' },
                    icon: 'question'
                }).then((result) => {
                    if (result.isConfirmed) { location.reload(true); }
                });

                // if (confirm('Вы ошиблись ' + error_count + ' раз(а). Желаете повторить?')) {
                //     location.reload();}
            }
            

        } else if (right == "") {
            if (left != mark) {
                document.getElementById(mark).style = light_style;
                document.getElementById(left).style = select_style;
                document.getElementById(left).style.color = "#000";

            }
            mark = id_word;
        } else if (left == "") {
            if (right != mark) {
                document.getElementById(mark).style = dark_style;
                document.getElementById(right).style = select_style;
                document.getElementById(right).style.color = "#FFF";
            }
            mark = id_word;
        } else if (left != "" || right != "") {
            error_count = error_count + 1;
            console.log(mark.slice(1));
            save_results(mark.slice(1), 1, 0);
            document.getElementById("errors_count").innerHTML = error_count;
            document.getElementById(left).style = error_style;
            document.getElementById(right).style = error_style;
            setTimeout(error_reset, 666, left, right);
            left = "";
            right = "";
            mark = "";
        }

    }

    window.remove = function (btn) {
        document.getElementById("zs1" + btn + "").style.opacity = 0.5;
        document.getElementById("zs1" + btn + "").style.pointerEvents = "none";
        document.getElementById("zs2" + btn + "").style.opacity = 0.5;
        document.getElementById("zs2" + btn + "").style.pointerEvents = "none";
    }

    window.error_reset = function (left, right) {
        document.getElementById(right).style = dark_style;
        document.getElementById(left).style = light_style;
    }
    /*игра конец*/
});
