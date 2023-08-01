jQuery(document).ready(function ($) {
    var loader = document.getElementById("preloader");
    var modaymisAddBtn = document.getElementById("modaymisUpload")
    var modaymisdUpdatetn = document.getElementById("modaymisUpdate")


    modaymisAddBtn.addEventListener("click", function () {
        loader.style.display = "flex";
        window.addEventListener("load", function () {
            loader.style.display = "none";
        })
    })

    modaymisdUpdatetn.addEventListener("click", function () {
        loader.style.display = "flex";
        window.addEventListener("load", function () {
            loader.style.display = "none";
        })
    })

});