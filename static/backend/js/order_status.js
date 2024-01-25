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

    document.getElementById("order_status").addEventListener('change', function () {
        $.ajax({
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            url: `/yonetim/siparis-yonetimi/siparisler/durum-guncelle/`,
            data: {
                'platform': $("#platform").val(),
                'siparis_no': $("input[name='siparisNo']").val(),
                'status': $(this).val(),
            },
            dataType: 'json',
            beforeSend: function () {
            },
            success: function (data) {
                if (data === 'success') {
                    iziToast.info({
                        title: 'Kayıt başarılı !',
                        message: 'Sipariş durumunu güncellendi.',
                        position: 'topRight'
                    });
                    setTimeout(function (){
                        window.location.reload()
                    },2000)
                }

            },
            error: function (e){
                iziToast.error({
                        title: 'Hata !',
                        message: `Bir hata meydana geldi. ${e}.`,
                        position: 'topRight'
                    });
            }
        });
    })

});