jQuery(document).ready(function ($) {
    var loader = document.getElementById("preloader");
    var AddBtn = document.getElementById("dataUpload")
    var Updatetn = document.getElementById("dataUpdate")


    AddBtn.addEventListener("click", function () {
        loader.style.display = "flex";
        window.addEventListener("load", function () {
            loader.style.display = "none";
        })
    })

    Updatetn.addEventListener("click", function () {
        loader.style.display = "flex";
        window.addEventListener("load", function () {
            loader.style.display = "none";
        })
    })

});