$(document).ready(function () {

    let allOrderDropdown = document.querySelectorAll('.order-dropdown')
    let allPlatformDropdown = document.querySelectorAll('.platform-dropdown')
    let allProfitDropdown = document.querySelectorAll('.profit-dropdown')

    allOrderDropdown.forEach((item) => {
        item.addEventListener('click', function (e) {
            if (this.classList.contains('selecting')) {
                this.classList.remove('selecting');
            } else {
                this.classList.add('selecting');
                allOrderDropdown.forEach(l => {
                    if (l !== this) {
                        l.classList.remove('selecting');
                    }
                });
            }

            $("#orders-month").text($(this).text())

            $.ajax({
                type: 'GET',
                url: `/yonetim/siparis-istatistikleri-ajax`,
                dataType: 'json',
                data: {
                    'ay': $(this).attr("data-value"),
                },
                beforeSend: function () {

                },
                success: function (data) {
                    $(".order-new-count").text(data[0])
                    $(".order-delivery-count").text(data[1])
                    $(".order-complated-count").text(data[2])
                }
            });
        })
    })

    allPlatformDropdown.forEach((item) => {
        item.addEventListener('click', function (e) {
            if (this.classList.contains('selecting')) {
                this.classList.remove('selecting');
            } else {
                this.classList.add('selecting');
                allPlatformDropdown.forEach(l => {
                    if (l !== this) {
                        l.classList.remove('selecting');
                    }
                });
            }

            $("#platform-month").text($(this).text())

            $.ajax({
                type: 'GET',
                url: `/yonetim/platform-istatistikleri-ajax`,
                dataType: 'json',
                data: {
                    'ay': $(this).attr("data-value"),
                },
                beforeSend: function () {

                },
                success: function (data) {
                    $(".platform-month-count").text(data[0])
                    $(".platform-tredyshop-count").text(data[1])
                    $(".platform-pazaryeri-count").text(data[2])
                }
            });
        })
    })


    $.ajax({
        type: 'GET',
        url: '/yonetim/kar-api/',
        beforeSend: function () {

        },
        success: (res) => {
            $(".total-profit").html(res[0].toFixed(2))
        }
    })

    $.ajax({
        type: 'GET',
        url: `/yonetim/kar-istatistikleri-ajax`,
        dataType: 'json',
        beforeSend: function () {

        },
        success: function (data) {
            $(".month-profit-count").text(data[0])
            $(".month-sales-count").text(data[1])
            $(".month-expenses-count").text(data[2])
        }
    });

    allProfitDropdown.forEach((item) => {
        item.addEventListener('click', function (e) {
            if (this.classList.contains('selecting')) {
                this.classList.remove('selecting');
            } else {
                this.classList.add('selecting');
                allProfitDropdown.forEach(l => {
                    if (l !== this) {
                        l.classList.remove('selecting');
                    }
                });
            }

            $("#profit-month").text($(this).text())

            $.ajax({
                type: 'GET',
                url: `/yonetim/kar-istatistikleri-ajax`,
                dataType: 'json',
                data: {
                    'ay': $(this).attr("data-value"),
                },
                beforeSend: function () {

                },
                success: function (data) {
                    $(".month-profit-count").text(data[0])
                    $(".month-sales-count").text(data[1])
                    $(".month-expenses-count").text(data[2])
                }
            });
        })
    })

    const daysTag = document.querySelector(".days"),
        currentDate = document.querySelector(".current-date"),
        prevNextIcon = document.querySelectorAll(".icons i");
// getting new date, current year and month
    let date = new Date(),
        currYear = date.getFullYear(),
        currMonth = date.getMonth();
// storing full name of all months in array
    const months = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
        "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"];
    const renderCalendar = () => {
        let firstDayofMonth = new Date(currYear, currMonth, 0).getDay(),
            lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate(),
            lastDayofMonth = new Date(currYear, currMonth, lastDateofMonth).getDay(),
            lastDateofLastMonth = new Date(currYear, currMonth, 0).getDate();
        let liTag = "";
        for (let i = firstDayofMonth; i > 0; i--) {
            liTag += `<li class="inactive">${lastDateofLastMonth - i + 1}</li>`;
        }
        for (let i = 1; i <= lastDateofMonth; i++) {
            let isToday = i === date.getDate() && currMonth === new Date().getMonth()
            && currYear === new Date().getFullYear() ? "active" : "";
            liTag += `<li class="${isToday}">${i}</li>`;
        }
        for (let i = lastDayofMonth; i < 6; i++) {
            liTag += `<li class="inactive">${i - lastDayofMonth + 1}</li>`
        }
        currentDate.innerText = `${months[currMonth]} ${currYear}`;
        daysTag.innerHTML = liTag;
    }
    renderCalendar();
    prevNextIcon.forEach(icon => {
        icon.addEventListener("click", () => {
            currMonth = icon.id === "prev" ? currMonth - 1 : currMonth + 1;
            if (currMonth < 0 || currMonth > 11) {
                date = new Date(currYear, currMonth, new Date().getDate());
                currYear = date.getFullYear();
                currMonth = date.getMonth();
            } else {
                date = new Date();
            }
            renderCalendar();
        });
    });

});