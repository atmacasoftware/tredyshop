var width = $(window).width();
const baseUrl = "127.0.0.1/"
$(window).resize(function () {
    if ($(window).width() <= 1199) {
        $(".search-result-box").addClass('search-sm')
        var inputWidth = $("#generalSearch").width() + 25
        $(".search-sm").css('width', `${inputWidth}`)

    }

    if ($(window).width() <= 992) {
        $(".cat_ust-giyim").hide()
        $(".cat_alt-giyim").hide()
        $(".cat_esofman-pijama").hide()
        $(".cat_ayakkabi").hide()
        $(".cat_ic-giyim").hide()
        $(".cat_elbise-tulum").hide()
        $(".cat_bebek").hide()
        $(".cat_aksesuar").hide()
        const navItemBtns = document.querySelectorAll(".departments-nav__item");
        navItemBtns.forEach((btn) => {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                var targetName = btn.getAttribute("target-name")
                console.log(targetName)
                if (targetName == "Üst Giyim") {
                    $(".cat_alt-giyim").hide()
                    $(".cat_esofman-pijama").hide()
                    $(".cat_ayakkabi").hide()
                    $(".cat_ic-giyim").hide()
                    $(".cat_elbise-tulum").hide()
                    $(".cat_bebek").hide()
                    $(".cat_aksesuar").hide()
                    $(".cat_ust-giyim").show()
                }
                if (targetName == "Alt Giyim") {
                    $(".cat_ust-giyim").hide()
                    $(".cat_esofman-pijama").hide()
                    $(".cat_ayakkabi").hide()
                    $(".cat_ic-giyim").hide()
                    $(".cat_elbise-tulum").hide()
                    $(".cat_bebek").hide()
                    $(".cat_aksesuar").hide()
                    $(".cat_alt-giyim").show()
                }
                if (targetName == "Eşofman Pijama") {
                    $(".cat_ust-giyim").hide()
                    $(".cat_alt-giyim").hide()
                    $(".cat_ayakkabi").hide()
                    $(".cat_ic-giyim").hide()
                    $(".cat_elbise-tulum").hide()
                    $(".cat_bebek").hide()
                    $(".cat_aksesuar").hide()
                    $(".cat_esofman-pijama").show()
                }

                if (targetName == "Elbise Tulum") {
                    $(".cat_ust-giyim").hide()
                    $(".cat_alt-giyim").hide()
                    $(".cat_esofman-pijama").hide()
                    $(".cat_ic-giyim").hide()
                    $(".cat_bebek").hide()
                    $(".cat_aksesuar").hide()
                    $(".cat_ayakkabi").hide()
                    $(".cat_elbise-tulum").show()
                }

                if (targetName == "Ayakkabı") {
                    $(".cat_ust-giyim").hide()
                    $(".cat_alt-giyim").hide()
                    $(".cat_esofman-pijama").hide()
                    $(".cat_ic-giyim").hide()
                    $(".cat_elbise-tulum").hide()
                    $(".cat_bebek").hide()
                    $(".cat_aksesuar").hide()
                    $(".cat_ayakkabi").show()
                }

                if (targetName == "İç Giyim") {
                    $(".cat_ust-giyim").hide()
                    $(".cat_alt-giyim").hide()
                    $(".cat_esofman-pijama").hide()
                    $(".cat_elbise-tulum").hide()
                    $(".cat_bebek").hide()
                    $(".cat_aksesuar").hide()
                    $(".cat_ayakkabi").hide()
                    $(".cat_ic-giyim").show()
                }

                if (targetName == "Bebek") {
                    $(".cat_ust-giyim").hide()
                    $(".cat_alt-giyim").hide()
                    $(".cat_esofman-pijama").hide()
                    $(".cat_elbise-tulum").hide()
                    $(".cat_aksesuar").hide()
                    $(".cat_ayakkabi").hide()
                    $(".cat_ic-giyim").hide()
                    $(".cat_bebek").show()
                }

                if (targetName == "Aksesuar") {
                    $(".cat_ust-giyim").hide()
                    $(".cat_alt-giyim").hide()
                    $(".cat_esofman-pijama").hide()
                    $(".cat_elbise-tulum").hide()
                    $(".cat_ayakkabi").hide()
                    $(".cat_ic-giyim").hide()
                    $(".cat_bebek").hide()
                    $(".cat_aksesuar").show()
                }

            })
        })
    } else {
        $(".cat_ust-giyim").show()
        $(".cat_alt-giyim").show()
        $(".cat_esofman-pijama").show()
        $(".cat_ayakkabi").show()
        $(".cat_ic-giyim").show()
        $(".cat_elbise-tulum").show()
        $(".cat_bebek").show()
        $(".cat_aksesuar").show()
    }
});

if (width <= 1199) {
    $(".search-result-box").addClass('search-sm')
    var inputWidth = $("#generalSearch").width() + 25
    console.log(inputWidth)
    $(".search-sm").css('width', `${inputWidth}`)
}

if (width <= 992) {
    $(".cat_ust-giyim").hide()
    $(".cat_alt-giyim").hide()
    $(".cat_esofman-pijama").hide()
    $(".cat_ayakkabi").hide()
    $(".cat_ic-giyim").hide()
    $(".cat_elbise-tulum").hide()
    $(".cat_bebek").hide()
    $(".cat_aksesuar").hide()
    const navItemBtns = document.querySelectorAll(".departments-nav__item");
    navItemBtns.forEach((btn) => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            var targetName = btn.getAttribute("target-name")
            if (targetName == "Üst Giyim") {
                $(".cat_alt-giyim").hide()
                $(".cat_esofman-pijama").hide()
                $(".cat_ayakkabi").hide()
                $(".cat_ic-giyim").hide()
                $(".cat_elbise-tulum").hide()
                $(".cat_bebek").hide()
                $(".cat_aksesuar").hide()
                $(".cat_ust-giyim").toggle("slow", function () {

                })
            }

            if (targetName == "Alt Giyim") {
                $(".cat_ust-giyim").hide()
                $(".cat_esofman-pijama").hide()
                $(".cat_ayakkabi").hide()
                $(".cat_ic-giyim").hide()
                $(".cat_elbise-tulum").hide()
                $(".cat_bebek").hide()
                $(".cat_aksesuar").hide()
                $(".cat_alt-giyim").toggle("slow", function () {

                })
            }

            if (targetName == "Eşofman Pijama") {
                $(".cat_ust-giyim").hide()
                $(".cat_ayakkabi").hide()
                $(".cat_ic-giyim").hide()
                $(".cat_elbise-tulum").hide()
                $(".cat_bebek").hide()
                $(".cat_aksesuar").hide()
                $(".cat_alt-giyim").hide()
                $(".cat_esofman-pijama").toggle("slow", function () {
                })
            }

            if (targetName == "Ayakkabi") {
                $(".cat_ust-giyim").hide()
                $(".cat_ic-giyim").hide()
                $(".cat_elbise-tulum").hide()
                $(".cat_bebek").hide()
                $(".cat_aksesuar").hide()
                $(".cat_alt-giyim").hide()
                $(".cat_esofman-pijama").hide()
                $(".cat_ayakkabi").toggle("slow", function () {
                })
            }

            if (targetName == "İç Giyim") {
                $(".cat_ust-giyim").hide()
                $(".cat_elbise-tulum").hide()
                $(".cat_bebek").hide()
                $(".cat_aksesuar").hide()
                $(".cat_alt-giyim").hide()
                $(".cat_esofman-pijama").hide()
                $(".cat_ayakkabi").hide
                $(".cat_ic-giyim").toggle("slow", function () {
                })
            }

            if (targetName == "Elbise Tulum") {
                $(".cat_ust-giyim").hide()
                $(".cat_bebek").hide()
                $(".cat_aksesuar").hide()
                $(".cat_alt-giyim").hide()
                $(".cat_esofman-pijama").hide()
                $(".cat_ayakkabi").hide
                $(".cat_ic-giyim").hide
                $(".cat_elbise-tulum").toggle("slow", function () {
                })
            }

            if (targetName == "Bebek") {
                $(".cat_ust-giyim").hide()
                $(".cat_aksesuar").hide()
                $(".cat_alt-giyim").hide()
                $(".cat_esofman-pijama").hide()
                $(".cat_ayakkabi").hide
                $(".cat_ic-giyim").hide
                $(".cat_elbise-tulum").hide()
                $(".cat_bebek").toggle("slow", function () {
                })
            }

            if (targetName == "Aksesuar") {
                $(".cat_ust-giyim").hide()
                $(".cat_alt-giyim").hide()
                $(".cat_esofman-pijama").hide()
                $(".cat_ayakkabi").hide
                $(".cat_ic-giyim").hide
                $(".cat_elbise-tulum").hide()
                $(".cat_bebek").hide
                $(".cat_aksesuar").toggle("slow", function () {
                })
            }

        })
    })
}

$(document).ready(function () {
    const topCat = document.querySelector('.main-header-section__topcatgs')
    $.ajax({
        url: `/apits/header-kategoriler/`,
        dataType: 'json',
        beforeSend: function () {

        },
        success: function (res) {
            var data = res.items
            data.forEach((item) => {
                topCat.innerHTML += `
                    <a href="${item.url}">
                            <span class="text">
                                ${item.title}
                            </span>
                    </a>
                `
            })

        }
    });
})