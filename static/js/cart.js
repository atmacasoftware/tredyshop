$(document).ready(function () {
    $("#approvedNote").hide();
    console.log($("textarea[name='preliminary_form']").val())
    $("#paymentBtn").on('click', function (e) {
        e.preventDefault();
        if ($("input[name='approved_contract']").is(':checked') === true) {
            $("#approvedNote").hide();
            var addres_id = $("input[name='selectedAddress']").val()
            var csrf_token = $("input[name='csrfmiddlewaretoken']").val()
            var approved = $("input[name='approved_contract']").val()
            var coupon = $("input[name='used_coupon']").val()
            var order_total = $("input[name='order_total']").val()
            var delivery_price = $("input[name='delivery_price']").val()
            var preliminary_form = $("textarea[name='preliminary_form']").val()
            var distance_selling_form = $("textarea[name='distance_selling_form']").val()
            var loader = document.getElementById("preloader");
            var checkout = $("#checkoutUrl").val()
            $.ajax({
                url: '/odeme-adimi',
                type: 'POST',
                data: {
                    'addres_id': addres_id,
                    'approved': approved,
                    'coupon': coupon,
                    'order_total': order_total,
                    'delivery_price': delivery_price,
                    'preliminary_form': preliminary_form,
                    'distance_selling_form': distance_selling_form,
                    'csrfmiddlewaretoken': csrf_token,
                },
                beforeSend: function () {
                    loader.style.display = 'flex'
                },
                success: function (data) {
                    loader.style.display = 'none'
                    if (data === 'success'){
                        window.location = checkout
                    }
                },
                error: function (error) {
                }
            })

        } else {
            $("#approvedNote").show();
            $(".approved-div").addClass('approved-alert', {duration: 1000})
            setTimeout(function () {
                $(".approved-div").removeClass('approved-alert', {duration: 1000})
            }, 3000);
        }
    })
});