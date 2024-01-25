"use strict";


$.ajax({
    type: 'GET',
    url: '/yonetim/son-yedi-gun-kar-api/',
    beforeSend: function () {

    },
    success: (res) => {

        var dates = res[0]
        var data = res[1]
        var spending = res[2]
        var kesintiler = res[3]
        var iadeler = res[4]
        var satislar = res[5]

        var ctx = document.getElementById("generalPerformance").getContext('2d');
        var generalPerformance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [dates[0], dates[1], dates[2], dates[3], dates[4], dates[5], dates[6]],
                datasets: [{
                    label: 'Satış',
                    data: [satislar[0].toFixed(2), satislar[1].toFixed(2), satislar[2].toFixed(2), satislar[3].toFixed(2), satislar[4].toFixed(2), satislar[5].toFixed(2), satislar[6].toFixed(2)],
                    borderWidth: 2,
                    backgroundColor: 'transparent',
                    borderColor: 'rgba(63,82,227,.8)',
                    pointBorderWidth: 0,
                    pointRadius: 3.5,
                    pointBackgroundColor: 'transparent',
                    pointHoverBackgroundColor: 'rgba(63,82,227,.8)',
                },
                    {
                        label: 'Harcama',
                        data: [spending[0].toFixed(2), spending[1].toFixed(2), spending[2].toFixed(2), spending[3].toFixed(2), spending[4].toFixed(2), spending[5].toFixed(2), spending[6].toFixed(2)],
                        borderWidth: 2,
                        backgroundColor: 'transparent',
                        borderColor: 'rgba(254,86,83,.8)',
                        pointBorderWidth: 0,
                        pointRadius: 3.5,
                        pointBackgroundColor: 'transparent',
                        pointHoverBackgroundColor: 'rgba(254,86,83,.8)',
                    },
                    {
                        label: 'Kesinti',
                        data: [kesintiler[0].toFixed(2), kesintiler[1].toFixed(2), kesintiler[2].toFixed(2), kesintiler[3].toFixed(2), kesintiler[4].toFixed(2), kesintiler[5].toFixed(2), kesintiler[6].toFixed(2)],
                        borderWidth: 2,
                        backgroundColor: 'transparent',
                        borderColor: 'rgba(246,217,74,0.7)',
                        pointBorderWidth: 0,
                        pointRadius: 3.5,
                        pointBackgroundColor: 'transparent',
                        pointHoverBackgroundColor: 'rgba(246,217,74,0.7)',
                    },
                    {
                        label: 'İade',
                        data: [iadeler[0].toFixed(2), iadeler[1].toFixed(2), iadeler[2].toFixed(2), iadeler[3].toFixed(2), iadeler[4].toFixed(2), iadeler[5].toFixed(2), iadeler[6].toFixed(2)],
                        borderWidth: 2,
                        backgroundColor: 'transparent',
                        borderColor: 'rgba(74,246,194,0.7)',
                        pointBorderWidth: 0,
                        pointRadius: 3.5,
                        pointBackgroundColor: 'transparent',
                        pointHoverBackgroundColor: 'rgba(74,246,194,0.7)',
                    },
                    {
                        type: 'line',
                        label: "Kar",
                        data: [data[0].toFixed(2), data[1].toFixed(2), data[2].toFixed(2), data[3].toFixed(2), data[4].toFixed(2), data[5].toFixed(2), data[6].toFixed(2)],
                        borderWidth: 2,
                        backgroundColor: 'transparent',
                        borderColor: 'rgba(0,255,42,0.7)',
                        pointBorderWidth: 0,
                        pointRadius: 3.5,
                        pointBackgroundColor: 'transparent',
                        pointHoverBackgroundColor: 'rgba(0,255,42,0.7)',
                    },
                ]
            },
            options: {
                legend: {
                    display: true
                },
                scales: {
                    yAxes: [{
                        gridLines: {
                            drawBorder: false,
                            color: '#f2f2f2',
                        },
                        ticks: {
                            beginAtZero: true,
                            callback: function (value, index, values) {
                                return value.toFixed(2) + ' ' + 'TL';
                            }
                        }
                    }],
                    xAxes: [{
                        gridLines: {
                            display: false,
                            tickMarkLength: 15,
                        }
                    }]
                },
            }
        });
        const paidGraph = document.getElementById('paidGraph');


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

    },
    success: (res) => {

        var sehir = res[0]
        var data = res[1]

        var ctx = document.getElementById("cityGraph").getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [sehir[0], sehir[1], sehir[2], sehir[3], sehir[4], sehir[5], sehir[6], sehir[7], sehir[8], sehir[9]],
                datasets: [{
                    label: 'Statistics',
                    data: [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[7], data[8], data[9]],
                    borderWidth: 2,
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
                    borderColor: 'transparent',
                    pointBackgroundColor: '#ffffff',
                    pointRadius: 4
                }]
            },
            options: {
                legend: {
                    display: false
                },
                scales: {
                    yAxes: [{
                        gridLines: {
                            drawBorder: false,
                            color: '#f2f2f2',
                        },
                        ticks: {
                            beginAtZero: true,
                            stepSize: 5
                        }
                    }],
                    xAxes: [{
                        ticks: {
                            display: true
                        },
                        gridLines: {
                            display: false
                        }
                    }]
                },
            }
        });

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

        var ctx = document.getElementById("marketPlaceStatisticsGraph").getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                datasets: [{
                    data: [tredyshopOrdersCount, trendyolOrdersCount, hepsiburadaOrdersCount, amazonOrdersCount],
                    backgroundColor: [
                        '#63ed7a',
                        '#ffa426',
                        '#fc544b',
                        '#6777ef',
                    ],
                    label: 'Dataset 1'
                }],
                labels: [
                    'TredyShop',
                    'Trendyol',
                    'Hepsiburada',
                    'Amazon',
                ],
            },
            options: {
                responsive: true,
                legend: {
                    position: 'bottom',
                },
            }
        });

    }
})

$.ajax({
    type: 'GET',
    url: '/yonetim/satislar-api/',
    beforeSend: function () {

    },
    success: (res) => {
        $("#dailySales").html(res[0] + " TL")
        $("#mountlySales").html(res[1] + " TL")
        $("#yearlySales").html(res[2] + " TL")

        var gunluk_degisim = parseFloat(res[5].toFixed(1))
        var aylik_degisim = parseFloat(res[6].toFixed(1))
        var yillik_degisim = parseFloat(res[7].toFixed(1))

        if (gunluk_degisim > 0) {
            $("#dailyStatistic").html(`
                    <span class="text-primary"><i
                                        class="fas fa-caret-up"></i></span>${gunluk_degisim}%
                `)
        } else if (gunluk_degisim < 0) {
            $("#dailyStatistic").html(`
                <span class="text-danger"><i
                                        class="fas fa-caret-down"></i></span> ${gunluk_degisim}%`)
        } else {
            $("#dailyStatistic").html(`<span class="text-dark"><i
                                        class="fas fa-fa-minus"></i></span> 0%`)
        }

        if (aylik_degisim > 0) {
            $("#mountlyStatistic").html(`<span class="text-primary"><i
                                        class="fas fa-caret-up"></i></span> ${aylik_degisim}%`)
        } else if (gunluk_degisim < 0) {
            $("#mountlyStatistic").html(`<span class="text-danger"><i
                                        class="fas fa-caret-down"></i></span> ${aylik_degisim}%`)
        } else {
            $("#mountlyStatistic").html(`<span class="text-dark"><i
                                        class="fas fa-minus"></i></span> 0%`)
        }

        if (yillik_degisim > 0) {
            $("#yearlyStatistic").html(`<span class="text-primary"><i
                                        class="fas fa-caret-up"></i></span> ${yillik_degisim}%`)
        } else if (gunluk_degisim < 0) {
            $("#yearlyStatistic").html(`<span class="text-danger"><i
                                        class="fas fa-caret-down"></i></span> ${yillik_degisim}%`)
        } else {
            $("#yearlyStatistic").html(`<span class="text-dark"><i
                                        class="fas fa-minus"></i></span> 0%`)
        }

    },
    error: (err) => {
        console.log(err)
    }
})

$("#products-carousel").owlCarousel({
    items: 3,
    margin: 10,
    autoplay: true,
    autoplayTimeout: 5000,
    loop: true,
    responsive: {
        0: {
            items: 2
        },
        768: {
            items: 2
        },
        1200: {
            items: 3
        }
    }
});
