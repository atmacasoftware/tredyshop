$(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: '/yonetim/satislar-api/',
        beforeSend: function () {
            $(".daily-sales-card .overlay").show()
            $(".mountly-sales-card .overlay").show()
            $(".yearly-sales-card .overlay").show()
        },
        success: (res) => {
            $(".daily-sales-card .overlay").hide()
            $(".mountly-sales-card .overlay").hide()
            $(".yearly-sales-card .overlay").hide()
            $("#dailySales").html(res[0].toFixed(2) + " TL")
            $("#mountlySales").html(res[1].toFixed(2) + " TL")
            $("#yearlySales").html(res[2].toFixed(2) + " TL")

            $(".yearly-sales-card .card-title").html(`${res[4]} Satışları`)

            if (res[3] == 1) {
                $(".mountly-sales-card .card-title").html("Ocak Satışları")
            } else if (res[3] == 2) {
                $(".mountly-sales-card .card-title").html("Şubat Satışları")
            } else if (res[3] == 3) {
                $(".mountly-sales-card .card-title").html("Mart Satışları")
            } else if (res[3] == 4) {
                $(".mountly-sales-card .card-title").html("Nisan Satışları")
            } else if (res[3] == 5) {
                $(".mountly-sales-card .card-title").html("Mayıs Satışları")
            } else if (res[3] == 6) {
                $(".mountly-sales-card .card-title").html("Haziran Satışları")
            } else if (res[3] == 7) {
                $(".mountly-sales-card .card-title").html("Temmuz Satışları")
            } else if (res[3] == 8) {
                $(".mountly-sales-card .card-title").html("Ağustos Satışları")
            } else if (res[3] == 9) {
                $(".mountly-sales-card .card-title").html("Eylül Satışları")
            } else if (res[3] == 10) {
                $(".mountly-sales-card .card-title").html("Ekim Satışları")
            } else if (res[3] == 11) {
                $(".mountly-sales-card .card-title").html("Kasım Satışları")
            } else if (res[3] == 12) {
                $(".mountly-sales-card .card-title").html("Aralık Satışları")
            }

            var gunluk_degisim = parseFloat(res[5].toFixed(1))
            var aylik_degisim = parseFloat(res[6].toFixed(1))
            var yillik_degisim = parseFloat(res[7].toFixed(1))

            if (gunluk_degisim > 0) {
                $("#dailyStatistic").html(`<i class="fa-solid fa-arrow-trend-up"></i> <small>%${gunluk_degisim}</small>`)
            } else if (gunluk_degisim < 0) {
                $("#dailyStatistic").html(`<i class="fa-solid fa-arrow-trend-down text-danger"></i> <small>%${gunluk_degisim}</small>`)
            } else {
                $("#dailyStatistic").html(`<i class="fa-solid fa-minus"></i> <small>%0.0</small>`)
            }

            if (aylik_degisim > 0) {
                $("#mountlyStatistic").html(`<i class="fa-solid fa-arrow-trend-up"></i> <small>%${aylik_degisim}</small>`)
            } else if (gunluk_degisim < 0) {
                $("#mountlyStatistic").html(`<i class="fa-solid fa-arrow-trend-down text-danger"></i> <small>%${aylik_degisim}</small>`)
            } else {
                $("#mountlyStatistic").html(`<i class="fa-solid fa-minus"></i> <small>%0.0</small>`)
            }

            if (yillik_degisim > 0) {
                $("#yearlyStatistic").html(`<i class="fa-solid fa-arrow-trend-up"></i> <small>%${yillik_degisim}</small>`)
            } else if (gunluk_degisim < 0) {
                $("#yearlyStatistic").html(`<i class="fa-solid fa-arrow-trend-down text-danger"></i> <small>%${yillik_degisim}</small>`)
            } else {
                $("#yearlyStatistic").html(`<i class="fa-solid fa-minus"></i> <small>%0.0</small>`)
            }

        },
        error: (err) => {
            console.log(err)
        }
    })
    $.ajax({
        type: 'GET',
        url: '/yonetim/kar-api/',
        beforeSend: function () {
            $(".total-revenue .overlay").show()
            $(".total-sales .overlay").show()
            $(".total-spending .overlay").show()
            $(".total-blackouts .overlay").show()
        },
        success: (res) => {
            $(".total-revenue .overlay").hide()
            $(".total-sales .overlay").hide()
            $(".total-spending .overlay").hide()
            $(".total-blackouts .overlay").hide()

            $(".total-revenue .info-box-number").html(res[0].toFixed(2) + " TL")
            $(".total-sales .info-box-number").html(res[1].toFixed(2) + " TL")
            $(".total-spending .info-box-number").html(res[2].toFixed(2) + " TL")
            $(".total-blackouts .info-box-number").html(res[3].toFixed(2) + " TL")

        },
        error: (err) => {
            $(".total-revenue .overlay").show()
            $(".total-sales .overlay").show()
            $(".total-spending .overlay").show()
            $(".total-blackouts .overlay").show()
        }
    })
    $.ajax({
        type: 'GET',
        url: '/yonetim/son-yedi-gun-kar-api/',
        beforeSend: function () {
            $("#lastSevenDayProfitCard .overlay").show()
            $("#lastSevenDayPaidCard .overlay").show()
        },
        success: (res) => {
            $("#lastSevenDayProfitCard .overlay").hide()
            $("#lastSevenDayPaidCard .overlay").hide()

            var dates = res[0]
            var data = res[1]
            var spending = res[2]
            var kesintiler = res[3]
            var iadeler = res[4]
            var satislar = res[5]

            const profitGraph = document.getElementById('profitGraph');

            new Chart(profitGraph, {
                type: 'line',
                data: {
                    labels: [dates[0], dates[1], dates[2], dates[3], dates[4], dates[5], dates[6]],
                    datasets: [{
                        label: 'Son 7 Günlük Kar Grafiği',
                        data: [data[0], data[1], data[2], data[3], data[4], data[5], data[6]],
                        backgroundColor: [
                            'rgba(66,246,6,0.2)',
                        ],
                        borderColor: [
                            'rgba(255,99,132,1)',
                            'rgba(54, 162, 235, 1)',
                        ],
                        borderWidth: 1
                    }]
                },

                options: {
                    maintainAspectRatio: true,
                }
            });

            const paidGraph = document.getElementById('paidGraph');

            new Chart(paidGraph, {
                type: 'bar',
                data: {
                    datasets: [{
                        type: 'bar',
                        label: "Kar",
                        data: [data[0], data[1], data[2], data[3], data[4], data[5], data[6]],
                        backgroundColor: [
                            'rgba(66,246,6,0.2)',
                            'rgba(66,246,6,0.2)',
                            'rgba(66,246,6,0.2)',
                            'rgba(66,246,6,0.2)',
                            'rgba(66,246,6,0.2)',
                            'rgba(66,246,6,0.2)',
                            'rgba(66,246,6,0.2)',
                        ],
                        borderColor: [
                            'rgba(54, 162, 235, 1)',
                        ],
                    }, {
                        type: 'line',
                        label: "Satış",
                        data: [satislar[0], satislar[1], satislar[2], satislar[3], satislar[4], satislar[5], satislar[6]],
                        backgroundColor: [
                            'rgba(0,0,0,0)',
                        ],
                        borderColor: [
                            'rgba(54, 162, 235, 1)',
                        ],
                    }, {
                        type: 'line',
                        label: "Harcama",
                        data: [spending[0], spending[1], spending[2], spending[3], spending[4], spending[5], spending[6]],
                        backgroundColor: [
                            'rgba(0,0,0,0)',
                        ],
                        borderColor: [
                            'rgb(255,63,6)',
                        ],
                    }, {
                        type: 'line',
                        label: "Kesinti",
                        data: [kesintiler[0], kesintiler[1], kesintiler[2], kesintiler[3], kesintiler[4], kesintiler[5], kesintiler[6]],
                        backgroundColor: [
                            'rgba(0,0,0,0)',
                        ],
                        borderColor: [
                            'rgb(230,6,255)',
                        ],
                    }, {
                        type: 'line',
                        label: "İade",
                        data: [iadeler[0], iadeler[1], iadeler[2], iadeler[3], iadeler[4], iadeler[5], iadeler[6]],
                        backgroundColor: [
                            'rgba(0,0,0,0)',
                        ],
                        borderColor: [
                            'rgb(255,251,6)',
                        ],
                    },
                    ],
                    labels: [dates[0], dates[1], dates[2], dates[3], dates[4], dates[5], dates[6]]
                },

                options: {
                    maintainAspectRatio: true,
                }
            });

        },
        error: (err) => {
            $("#lastSevenDayProfitCard .overlay").show()
            $("#lastSevenDayPaidCard .overlay").show()
        }
    })
    $.ajax({
        type: 'GET',
        url: '/yonetim/en-cok-siparis-gelen-10-sehir/',
        beforeSend: function () {
            $("#mostOrderTenCityCard .overlay").show()
        },
        success: (res) => {
            $("#mostOrderTenCityCard .overlay").hide()
            var sehir = res[0]
            var data = res[1]

            const cityGraph = document.getElementById('cityGraph');

            new Chart(cityGraph, {
                type: 'bar',
                data: {
                    labels: [sehir[0], sehir[1], sehir[2], sehir[3], sehir[4], sehir[5], sehir[6], sehir[7], sehir[8], sehir[9]],
                    datasets: [{
                        label: "En Çok Sipariş Gelen 10 Şehir",
                        data: [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[7], data[8], data[9]],
                        backgroundColor: [
                            'rgba(66,246,6,0.2)',
                            'rgb(239,134,134)',
                            'rgb(7,89,203)',
                            'rgba(6,246,202,0.2)',
                            'rgba(90,125,241,0.2)',
                            'rgba(210,56,111,0.2)',
                            'rgba(46,97,204,0.34)',
                            'rgba(246,114,6,0.2)',
                            'rgba(202,6,246,0.2)',
                            'rgba(246,242,6,0.2)',
                        ],
                        borderWidth: 1,
                    }]
                },

                options: {
                    maintainAspectRatio: true,
                }
            });

        },
        error: (err) => {
            $("#mostOrderTenCityCard .overlay").show()
        }
    })
    $.ajax({
        type: 'GET',
        url: '/yonetim/pazaryerleri-satis-istatistikleri/',
        beforeSend: function () {
            $("#marketPlaceStatistics .overlay").show()
        },
        success: (res) => {
            $("#marketPlaceStatistics .overlay").hide()
            var tredyshopOrdersCount = res[0]
            var trendyolOrdersCount = res[1]
            var hepsiburadaOrdersCount = res[2]
            var amazonOrdersCount = res[3]

            $("#tredyshopOrderCount").html(tredyshopOrdersCount)
            $("#trendyolOrderCount").html(trendyolOrdersCount)
            $("#hepsiburadaOrderCount").html(hepsiburadaOrdersCount)
            $("#amazonOrderCount").html(amazonOrdersCount)

            const marketPlaceStatisticsGraph = document.getElementById('marketPlaceStatisticsGraph');

            new Chart(marketPlaceStatisticsGraph, {
                type: 'doughnut',
                data: {
                    labels: ["TredyShop", "Trendyol", "Hepsiburada", "Amazon"],
                    datasets: [{
                        label: "Pazaryerleri Satış İstatistikleri",
                        data: [tredyshopOrdersCount, trendyolOrdersCount, hepsiburadaOrdersCount, amazonOrdersCount],
                        backgroundColor: [
                            '#dc3545',
                            '#fd7e14',
                            '#28a745',
                            '#000',
                        ],
                        borderWidth: 1,
                    }]
                },
            });

        },
        error: (err) => {
            $("#mostOrderTenCityCard .overlay").show()
        }
    })
});