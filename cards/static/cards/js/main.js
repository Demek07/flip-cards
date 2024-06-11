/*игра начало*/
let mark = "";
let left = "";
let right = "";
// let remains = 10;
let remains = parseInt(document.getElementById("remains").innerHTML);
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
            console.log(id);
            console.log(user_id);
            remove(id);
        }, 333);
        if ((remains == 0) & ( error_count == 0)) {
            if (confirm('Вы без ошибок определили все пары! Желаете повторить?')) {
                location.reload();}
        } else if ((remains == 0) & (error_count != 0)) {
            if (confirm('Вы ошиблись ' + error_count + ' раз(а). Желаете повторить?')) {
                location.reload();}
        }
        

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
        console.log(id);
        console.log(user_id);
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
/*игра конец*/
