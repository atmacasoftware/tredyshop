const cookieBox = document.querySelector(".cookie__wrapper"),
    button = document.getElementById("cookieAcceptBtn");

const executeCodes = () => {
    if(document.cookie.includes("tredyshop")) return;
    cookieBox.classList.add("show");

    button.addEventListener("click", () => {
        cookieBox.classList.remove("show");
        document.cookie = "cookie= tredyshop; max-age=" + 60 * 60 * 24 * 30;
    })

};
window.addEventListener("load", executeCodes);