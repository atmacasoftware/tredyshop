const cookieBox = document.querySelector(".cookie-wrapper");
const acceptBtn = document.getElementById("cookieAcceptBtn");
const declineBtn = document.getElementById("cookieDeclineBtn");
const settingBtn = document.getElementById("cookieSettingBtn");
const cookieWrapper = document.getElementById("cookieWrapper");
const cookieModal = document.getElementById("cookie-modal");
const functionalityCheck = document.getElementById("functionalityCheck");
const marketingCheck = document.getElementById("marketingCheck");
const performanceCheck = document.getElementById("performanceCheck");
const settingAcceptBtn = document.getElementById("settingAcceptBtn");
const modelClose = document.querySelector(".close-btn");
var isfunctionalityCheck = false
var ismarketingCheck = false
var isperformanceCheck = false

settingBtn.addEventListener('click', function () {
    cookieWrapper.style.display = "block";
    cookieWrapper.classList.add("open");
    cookieModal.classList.add("show");
});


modelClose.addEventListener("click", function () {
    cookieWrapper.classList.remove("open");
    cookieModal.classList.remove("show");
})

if (document.cookie.includes("tredyShop")) {
    cookieBox.classList.add('hide');
}


//İşlevsellik Çerezleri
if (document.cookie.includes("functionalityCheck")) {
    functionalityCheck.setAttribute("checked", "checked")
}
functionalityCheck.addEventListener('change', function () {
    isfunctionalityCheck = $(this).is(':checked')
    if (isfunctionalityCheck == true) {
        document.cookie = "functionalityCheck=True"
    }
    if (isfunctionalityCheck == false) {
        document.cookie = "functionalityCheck=True;expires=sat 1 jan 2000 12:00:00 UTC"
    }

})


//Hedefleme/Pazarlama Çerezleri
if (document.cookie.includes("marketingCheck")) {
    marketingCheck.setAttribute("checked", "checked")
}
marketingCheck.addEventListener('change', function () {
    ismarketingCheck = $(this).is(':checked')

    if (ismarketingCheck == true) {
        document.cookie = "marketingCheck=True"
    }
    if (ismarketingCheck == false) {
        document.cookie = "marketingCheck=True;expires=sat 1 jan 2000 12:00:00 UTC"
    }
})


//Performans Çerezleri
if (document.cookie.includes("performanceCheck")) {
    performanceCheck.setAttribute("checked", "checked")
}


if (document.cookie.includes("performanceCheck") == false) {
    Cookies.remove('_ga_7WERTPZR5T', {path: ''})
    Cookies.remove('_ga', {path: ''})
    Cookies.remove('_ga_TJV44SP27Y', {path: ''})
}


performanceCheck.addEventListener('change', function () {
    isperformanceCheck = $(this).is(':checked')

    if (isperformanceCheck == true) {
        document.cookie = "performanceCheck=True"
    }
    if (isperformanceCheck == false) {
        document.cookie = "performanceCheck=True;expires=sat 1 jan 2000 12:00:00 UTC"
    }
})


if (document.cookie.includes("performanceCheck") && document.cookie.includes("marketingCheck") && document.cookie.includes("functionalityCheck")) {
    cookieBox.classList.add('hide');
}

acceptBtn.addEventListener('click', function () {
    document.cookie = "cookieBy= tredyShop; max-age=" + 60 * 60 * 24 * 30;
    document.cookie = "performanceCheck=True"
    document.cookie = "marketingCheck=True"
    document.cookie = "functionalityCheck=True"
    cookieBox.classList.add('hide');
    location.reload();
});


declineBtn.addEventListener('click', function () {
    document.cookie = "cookieBy= tredyShop;expires=sat 1 jan 2000 12:00:00 UTC";
    document.cookie = "deneme= deneme;expires=sat 1 jan 2000 12:00:00 UTC";
    document.cookie = "performanceCheck=True;expires=sat 1 jan 2000 12:00:00 UTC"
    document.cookie = "marketingCheck=True;expires=sat 1 jan 2000 12:00:00 UTC"
    document.cookie = "functionalityCheck=True;expires=sat 1 jan 2000 12:00:00 UTC"
    Cookies.remove('_ga_7WERTPZR5T', {path: ''})
    Cookies.remove('_ga', {path: ''})
    Cookies.remove('_ga_TJV44SP27Y', {path: ''})
    location.reload();
});


settingAcceptBtn.addEventListener('click', function (){
   location.reload();
});



