$(document).ready(function () {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    $(".waiting").hide();
    var order_number = $("#orderNumber").text()

    document.getElementById("shippingInformationBtn").addEventListener('click', function () {
        $.ajax({
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            url: `/yonetim/siparis-yonetimi/siparisler/siparis_no=${order_number}/kargo-bildir/`,
            data: {
                'kargo_firmasi': $("select[name='deliveryCompany']").find(":selected").val(),
                'takip_numarasi': $("input[name='trackNumber']").val(),
                'takip_linki': $("input[name='takipLinki']").val(),
            },
            dataType: 'json',
            beforeSend: function () {
                $(".waiting").show();
            },
            success: function (data) {
                $(".waiting").hide();
                window.location.reload()

            }
        });
    })
    document.getElementById("shippingInformationUpdateBtn").addEventListener('click', function () {
        $.ajax({
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            url: `/yonetim/siparis-yonetimi/siparisler/siparis_no=${order_number}/kargo-bildir/`,
            data: {
                'kargo_firmasi': $("select[name='deliveryUpdateCompany']").find(":selected").val(),
                'takip_numarasi': $("input[name='trackNumberUpdate']").val(),
                'takip_linki': $("input[name='takipLinkiUpdate']").val(),
            },
            dataType: 'json',
            beforeSend: function () {
                $(".waiting").show();
            },
            success: function (data) {
                $(".waiting").hide();
                window.location.reload()

            }
        });
    })

});