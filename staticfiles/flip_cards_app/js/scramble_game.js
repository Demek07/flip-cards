document.addEventListener('DOMContentLoaded', function() {
    // Variables
    let currentWord = "";
    let timeLeft = 30;
    let timer;
    
    const wordElement = document.querySelector(".word");
    const hintElement = document.querySelector(".hint span");
    const timeLeftElement = document.querySelector(".hint strong");
    const inputField = document.getElementById("input");
    const shuffleButton = document.getElementById("btn_new");
    const submitButton = document.getElementById("btn_check");

    // Function to start a new round
    function newRound() {
        currentWord = document.querySelector('.content').id;
        timeLeft = 30;
        inputField.value = "";
        inputField.removeAttribute("disabled");
        submitButton.removeAttribute("disabled");
        clearInterval(timer);
        timer = setInterval(updateTimeLeft, 1000);
    }

    // Function to update the time left
    function updateTimeLeft() {
        if (timeLeft <= 0) {
            clearInterval(timer);
            inputField.setAttribute("disabled", "disabled");
            submitButton.setAttribute("disabled", "disabled");
            calert({
                confirmButton: { innerText: 'Да', style: { background: '#68539E' } },
                cancelButton: 'Нет',
                title: "Время вышло!",
                text: { innerHTML: `<b> ${currentWord.toUpperCase()}</b> - является правильным словом! <br> Желаете сыграть еще раз?` },
                icon: 'error'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.reload(true);
                    newRound();
                }
            });
        } else {
            timeLeft--;
            timeLeftElement.textContent = `${timeLeft} сек`;
        }
    }

    // Event listeners
    if (shuffleButton) {
        shuffleButton.addEventListener("click", function () {
            window.location.reload(true);
            newRound();
        });
    }

    if (submitButton) {
        submitButton.addEventListener("click", function () {
            const userGuess = inputField.value;
            
            if (!userGuess) return calert({ 
                confirmButton: {style: {background: '#68539E'}}, 
                title: "Пожалуйста введите слово!", 
                icon: "error" 
            });

            if (userGuess.toUpperCase() === currentWord.toUpperCase()) {
                clearInterval(timer);
                inputField.setAttribute("disabled", "disabled");
                submitButton.setAttribute("disabled", "disabled");
                calert({
                    confirmButton: { innerText: 'Да', style: { background: '#68539E' } },
                    cancelButton: 'Нет',
                    title: "Поздравляем!",
                    text: { innerHTML: `<b> ${userGuess.toUpperCase()}</b> - это правильное слово! <br> Желаете сыграть еще раз?` },
                    icon: 'success'
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.reload(true);
                        newRound();
                    }
                });
            } else {
                calert({
                    confirmButton: {style: {background: '#68539E'}},
                    title: `${userGuess.toUpperCase()}`,
                    text: 'это неправильное слово!',
                    icon: 'warning'
                });    
            }
        });
    }

    // Initialize the game with the first word
    if (inputField && submitButton && document.querySelector('.content')) {
        newRound();
    }
});