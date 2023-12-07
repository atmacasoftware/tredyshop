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

    document.getElementById("coastAdd").addEventListener('click', function () {
        $.ajax({
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            url: `/yonetim/ajax-urun-alimi/harcama/ekle/`,
            data: {
                'siparis_no': $("input[name='siparisNo']").val(),
                'harcama_adi': $("input[name='harcamaAdi']").val(),
                'harcama_tutari': $("input[name='harcamaTutari']").val(),
                'harcama_not': $("input[name='harcamaNot']").val(),
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