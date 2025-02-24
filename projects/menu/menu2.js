var today = new Date();
//var today = new Date(2023, 6, 22);//testing
var d = String(today.getDate());
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();

var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
var month = months[today.getMonth()];

var days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
var day = days[today.getDay()];



//should get date in Eastern time
//week 1 starts 8/19/2023 -- moved to Saturday so the next week will show up on the weekend.
week1 = new Date(2023, 7, 19);//month is 0 indexed, = Saturday August 19 
var Diff_days = Math.floor((today - week1) / (1000 * 60 * 60 * 24));
//console.log(today);
//console.log(week1);
//console.log(Diff_days);
week = (Math.floor(Diff_days / 7)) % 4 + 1; //Floor then add 1 to get weeks 1-4 (not 0-3)
console.log(week);

//document.getElementById("test").innerHTML = today;
document.getElementById("todayIs").innerHTML = "Today is "+day+", "+month+" "+d+", "+yyyy+".";

if(day=="Saturday" || day=="Sunday"){
	document.getElementById("todayIs").innerHTML += " Consult Week "+week+" for the next meal.";
}

window.onload = function () {
    switch (week) {
        case 1:
            var elements = document.getElementsByClassName("first");
            var non = document.querySelectorAll('.second,.thirdo,.fourth');
            break;
        case 2:
            var elements = document.getElementsByClassName("second");
            var non = document.querySelectorAll('.first,.thirdo,.fourth');
            break;
        case 3:
            var elements = document.getElementsByClassName("thirdo");
            var non = document.querySelectorAll('.first,.second,.fourth');
            break;
        case 4:
            var elements = document.getElementsByClassName("fourth");
            var non = document.querySelectorAll('.first,.second,.thirdo');
            break;
        default:
            var elements = [];
            var non = [];
    }
    switch (day) {
        case "Monday":
            var colElements = document.getElementsByClassName("m");
            break;
        case "Tuesday":
            var colElements = document.getElementsByClassName("t");
            break;
        case "Wednesday":
            var colElements = document.getElementsByClassName("w");
            break;
        case "Thursday":
            var colElements = document.getElementsByClassName("h");
            break;
        case "Friday":
            var colElements = document.getElementsByClassName("f");
            break;
        default:
            var colElements = [];
    }
    for (var i = 0; i < elements.length; i++) {
        elements[i].classList.add('hlight');
    }
    for (var i = 0; i < colElements.length; i++) {
        colElements[i].classList.add('daylight');
    }
    for (var i = 0; i < non.length; i++) {
        non[i].classList.add('dimRow');
    }

   
}

var lastModificationDate = new Date(document.lastModified);
document.getElementById("update").innerHTML = "Page last updated: " + lastModificationDate;