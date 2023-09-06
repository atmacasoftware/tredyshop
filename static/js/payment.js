$(document).ready(function () {

    $("input[name='payment_type']").on('click', function () {

        if ($(this).val() === 'transfer') {
            $("#paymentType").html("Havale");
            $("#id_cardholder").removeAttr("required")
            $("#cardnumber").removeAttr("required")
            $("#expiration").removeAttr("required")
            $("#cvv").removeAttr("required")
            $("#transferIcon").html(`<i class="fa-solid fa-chevron-up"></i>`)
            $("#crediCartIcon").html(`<i class="fa-solid fa-chevron-down"></i>`)
        } else {
            $("#paymentType").html("Banka/Kredi Kartı")
            $("#id_cardholder").attr("required", true)
            $("#cardnumber").attr("required", true)
            $("#expiration").attr("required", true)
            $("#cvv").attr("required", true)
            $("#transferIcon").html(`<i class="fa-solid fa-chevron-down"></i>`)
            $("#crediCartIcon").html(`<i class="fa-solid fa-chevron-up"></i>`)
        }
    });

});
