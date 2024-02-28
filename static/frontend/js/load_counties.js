$(document).ready(function () {
    $("#id_city").change(function () {
        const url = $("#addAddressForm").attr("data-counties-url");
        const cityId = $(this).val();

        $.ajax({
            url: url,
            data: {
                'city_id': cityId
            },
            success: function (data) {
                $("#id_county").html(data);
            }
        });

    });
})