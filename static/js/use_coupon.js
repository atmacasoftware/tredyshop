$(document).ready(function () {
    $("#deleteCoupon").hide();

    var current_total = $("#total-price").text()

    $("#getCoupon").click(function (e) {
        e.preventDefault();

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        $.ajax({
            url: `/kupon-uygula`,
            type: 'POST',
            data: {
                'code': $("#coupon").val(),
                csrfmiddlewaretoken: csrftoken
            },
            success: function (data) {
                console.log(data.data)
                if (data.data === 'none') {
                    $("#coupon").val("Böyle bir kupon bulunamadı.")
                } else {
                    if (parseFloat(current_total) > parseFloat(data.data.condition)) {
                        $("#deleteCoupon").removeClass('coupon-active')
                        $("#deleteCoupon").addClass('coupon-active')
                        $("#getCoupon").addClass('coupon-passive');
                        $("#coupon").val(data.data.name)
                        $(".coupon").text(`${data.data.price} TL`)
                        $("#total-price").text(`${(parseFloat(current_total) - parseFloat(data.data.price)).toFixed(2)} TL`)
                    } else {
                        $("#coupon").val("Kupon şartları sağlanmıyor.")
                    }
                }
            },
            error: function (error) {
                console.log(error)
            }
        })
    })

    $("#deleteCoupon").click(function (e) {
        e.preventDefault();
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            url: `/kupon-kaldir`,
            type: 'POST',
            data: {
                'code': $("#coupon").val(),
                csrfmiddlewaretoken: csrftoken
            },
            success: function (data) {
                $("#deleteCoupon").removeClass('coupon-active')
                $("#deleteCoupon").addClass('coupon-passive')
                $("#getCoupon").removeClass('coupon-passive');

                $(".coupon").text('')
                $("#total-price").text(`${(parseFloat(current_total)).toFixed(2)} TL`)
            },
            error: function (error) {
                console.log(error)
            }
        })

    })
})

