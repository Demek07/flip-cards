const wordText = document.querySelector(".word"),
hintText = document.querySelector(".hint span"),
timeText = document.querySelector(".time b"),
inputField = document.querySelector("input"),
refreshBtn = document.querySelector(".refresh-word"),
checkBtn = document.querySelector(".check-word");

let timer;

const initTimer = maxTime => {
    clearInterval(timer);
    timer = setInterval(() => {
        if(maxTime > 0) {
            maxTime--;
            return timeText.innerText = maxTime;
        }
        alert(`Время вышло! ${correctWord.toUpperCase()} является правильным словом!`);
        window.location.reload(true);
        initGame();
    }, 1000);
}

const initGame = () => {
    initTimer(30);
    // window.location.reload(true);
    correctWord = document.querySelector('.content').id;
    console.log(correctWord);
    inputField.value = "";
    inputField.setAttribute("maxlength", correctWord.length);
}
initGame();

const checkWord = () => {
    // let userWord = inputField.value.toLowerCase();
    let userWord = inputField.value;
    console.log(userWord);
    if(!userWord) return alert("Пожалуйста введите слово!");
    if(userWord !== correctWord) return alert('Упссс! ${userWord} это не правильное слово!');
    alert(`Поздравляю! ${correctWord.toUpperCase()} является правильным словом!`);
    initGame();
}

refreshBtn.addEventListener("click", initGame);
checkBtn.addEventListener("click", checkWord);