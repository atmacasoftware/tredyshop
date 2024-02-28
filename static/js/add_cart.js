$(document).ready(function () {
    var product_id = $("#product_id").val()
    var variant_id = $("#generalVariantId").val()
    var quantity = 1

    var maxQuantity = $("#quantity").attr('max')

    $(".js-plus").click(function () {
        quantityInput = $("#quantity").val()
        if (quantityInput < maxQuantity){
            quantity = parseInt(quantityInput) + 1
        }

    })

    $(".js-minus").click(function () {
        quantityInput = $("#quantity").val()
        quantity = parseInt(quantityInput) - 1
        if (quantity < 1) {
            quantity = 1
        }
    })

    $("#waitingCard").hide()
    $(".cart-popup").remove('open')
    $(".quick-modal").remove('show')

    $("#addingCard").click(function (e) {

        e.preventDefault()
        $.ajax({
            url: `/urun_ekle/${product_id}`,
            type: 'GET',
            data: {
                'product_id': product_id,
                'quantity': quantity,
                'variantid': variant_id
            },
            beforeSend: function () {
                $("#addingCard").hide()
                $(".e-quantity").hide()

            },
            success: function (data) {
                $("#waitingCard").show()
                $("#addingCard").hide()
                $(".cart-popup").addClass('open')
                $(".quick-modal").addClass('show')


                setTimeout(function () {
                    $("#waitingCard").hide()
                    $("#addingCard").show()
                    $(".e-quantity").show()
                }, 2000);

            },
            error: function (error) {
                $(".cart-popup").removeClass('open')
                $(".quick-modal").removeClass('show')
            }
        })
    })



})
