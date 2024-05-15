let mark = "";
let left = "";
let right = "";
let remains = 10;
let id = "";
let error_count = 0;
let error_style = `
    background-color: #BF3740;
    border-color : #B9242D;`
let correct_style = `
    background-color: #73A720;
    border-color : #68961D;`
let select_style = `
    background-color: #3F88C5;
    border-color : #3A7CB4;`
let light_style = `
    background-color: #FFF;
    border-color : #CCC;
    color: #666;`
let dark_style = `
    background-color: #1d2731;
    border-color : #1d2731;
    color: #FFF;`    


function click1(id_card) {
    console.log(remains);
    id = id_card.slice(1);
    if (id_card[0] == "l") {
        left = id_card;
    } else if (id_card[0] == "r") {
        right = id_card;
    }
    if (mark == "") {
        mark = id_card;
    }
    document.getElementById(mark).style = select_style;
    if (left.slice(1) == right.slice(1)) {
        remains = remains - 1;
        document.getElementById(left).style = correct_style;
        document.getElementById(right).style = correct_style;
        document.getElementById("remains").innerHTML = remains;
        mark = "";
        left = "";
        right = "";
        setTimeout(function () {
            remove(id);
        }, 333);
    } else if (right == "") {
        if (left != mark) {
            document.getElementById(mark).style = light_style;
            document.getElementById(left).style = select_style;
            document.getElementById(left).style.color = "#000";

        }
        mark = id_card;
    } else if (left == "") {
        if (right != mark) {
            document.getElementById(mark).style = dark_style;
            document.getElementById(right).style = select_style;
            document.getElementById(right).style.color = "#FFF";
        }
        mark = id_card;
    } else if (left != "" || right != "") {
        error_count = error_count + 1;
        document.getElementById("errors_count").innerHTML = error_count;
        document.getElementById(left).style = error_style;
        document.getElementById(right).style = error_style;
        setTimeout(error_reset, 666, left, right);
        left = "";
        right = "";
        mark = "";
    }

}

function remove(btn) {
    document.getElementById("zs1" + btn + "").style.opacity = 0.5;
    document.getElementById("zs1" + btn + "").style.pointerEvents = "none";
    document.getElementById("zs2" + btn + "").style.opacity = 0.5;
    document.getElementById("zs2" + btn + "").style.pointerEvents = "none";

}
function error_reset(left, right) {
    document.getElementById(right).style = dark_style;
    document.getElementById(left).style = light_style;
}
// cards/static/cards/js/main.js
// Главный файл для всего приложения, подключается в шаблоне base.html


// $(document).ready(function() {
//     $( ".mr-auto .nav-item" ).bind( "click", function(event) {
//         event.preventDefault();
//         var clickedItem = $( this );
//         $( ".mr-auto .nav-item" ).each( function() {
//             $( this ).removeClass( "active" );
//         });
//         clickedItem.addClass( "active" );
//     });
// });

const wrapper = document.querySelector(".wrapper"),
searchInput = wrapper.querySelector("input"),
volume = wrapper.querySelector(".word i"),
infoText = wrapper.querySelector(".info-text"),
synonyms = wrapper.querySelector(".synonyms .list"),
removeIcon = wrapper.querySelector(".search span");
let audio;

function data(result, word){
    if(result.title){
        infoText.innerHTML = `Не могу найти перевод для слова <span>"${word}"</span>. Пожалуйста, попробуйте поискать другое слово.`;
    }else{
        wrapper.classList.add("active");
        let definitions = result[0].meanings[0].definitions[0],
        phontetics = `${result[0].meanings[0].partOfSpeech}  /${result[0].phonetics[0].text}/`;
        document.querySelector(".word p").innerText = result[0].word;
        document.querySelector(".word span").innerText = phontetics;
        document.querySelector(".meaning span").innerText = definitions.definition;
        document.querySelector(".example span").innerText = definitions.example;
        audio = new Audio(result[0].phonetics[0].audio);

        if(definitions.synonyms[0] == undefined){
            synonyms.parentElement.style.display = "none";
        }else{
            synonyms.parentElement.style.display = "block";
            synonyms.innerHTML = "";
            for (let i = 0; i < 5; i++) {
                let tag = `<span onclick="search('${definitions.synonyms[i]}')">${definitions.synonyms[i]},</span>`;
                tag = i == 4 ? tag = `<span onclick="search('${definitions.synonyms[i]}')">${definitions.synonyms[4]}</span>` : tag;
                synonyms.insertAdjacentHTML("beforeend", tag);
            }
        }
    }
}

function search(word){
    fetchApi(word);
    searchInput.value = word;
}

function fetchApi(word){
    wrapper.classList.remove("active");
    infoText.style.color = "#000";
    infoText.innerHTML = `Ищу перевод для <span>"${word}"</span>`;
    let url = `https://api.dictionaryapi.dev/api/v2/entries/en/${word}`;
    fetch(url).then(response => response.json()).then(result => data(result, word)).catch(() =>{
        infoText.innerHTML = `Не могу найти перевод для слова <span>"${word}"</span>. Пожалуйста, попробуйте поискать другое слово.`;
    });
}

searchInput.addEventListener("keyup", e =>{
    let word = e.target.value.replace(/\s+/g, ' ');
    if(e.key == "Enter" && word){
        fetchApi(word);
    }
});

volume.addEventListener("click", ()=>{
    volume.style.color = "#4D59FB";
    audio.play();
    setTimeout(() =>{
        volume.style.color = "#999";
    }, 800);
});

removeIcon.addEventListener("click", ()=>{
    searchInput.value = "";
    searchInput.focus();
    wrapper.classList.remove("active");
    infoText.style.color = "#9A9A9A";
    infoText.innerHTML = "Введите любое слово и нажмите Enter, чтобы получить перевод.";
});
