window.setTimeout(function() {
    $(".alert").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });
}, 4000);

$('ul.nav li.dropdown').hover(function() {
  $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeIn(250);
}, function() {
  $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeOut(250);
});

var menu_btn = document.querySelector("#menu-btn");
var sidebar = document.querySelector("#sidebar");
var container = document.querySelector(".my-container");
var logo = document.querySelector(".logo-side");
menu_btn.addEventListener("click", () => {
  sidebar.classList.toggle("active-nav");
});
