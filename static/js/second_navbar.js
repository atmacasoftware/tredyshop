$(document).ready(function () {
    $("header#main-nav-header").find("button#catgmenu-btn").on('click', function (event) {
        event.preventDefault();
        $("header#main-nav-header").toggleClass("catgmenu-open");


        if ($(this).hasClass("catalog-btn__closed")) {
            $(this).removeClass("catalog-btn__closed").addClass("catalog-btn__open");
        } else {
            $(this).removeClass("catalog-btn__open").addClass("catalog-btn__closed");
        }
    });
})
