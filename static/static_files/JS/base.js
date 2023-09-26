/* Добавляет/удаляет класс "responsive" в панель навигации,
 когда пользователь нажимает на иконку */
function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}