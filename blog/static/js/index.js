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

var menu_btn_open = document.querySelector("#menu-btn-open");
var menu_btn_close = document.querySelector("#menu-btn-close");
var sidebar = document.querySelector("#sidebar");
var container = document.querySelector(".my-container");
var logo_main = document.querySelector(".logo-main");
var sb1 = document.querySelector(".sb-1");
var sb2 = document.querySelector(".sb-2");
var sb_search = document.querySelector("form");
var header_dark = document.querySelector("header");
var main_dark = document.querySelector("main");
var logo_dark = document.querySelector("a");

menu_btn_open.addEventListener("click", () => {
  sidebar.classList.toggle("active-nav");
  sb1.classList.toggle("ps-3");
  sb2.classList.toggle("ps-3");
  sb_search.classList.toggle("px-3");
  main_dark.classList.toggle("site-dark");
});

menu_btn_close.addEventListener("click", () => {
  sidebar.classList.toggle("active-nav");
  sb1.classList.toggle("ps-3");
  sb2.classList.toggle("ps-3");
  sb_search.classList.toggle("px-3");
  main_dark.classList.toggle("site-dark");
});
