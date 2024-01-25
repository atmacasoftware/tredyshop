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

const addHepsiburadaOrderBtn = document.getElementById("hepsiburadaOrderaddBtn");
addHepsiburadaOrderBtn.addEventListener('click', function (e) {
    e.preventDefault();

    $.ajax({
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        url: `/yonetim/siparis-yonetimi/hepsiburada-siparisler/siparis-ekle/`,
        data: {
            'h_order_number': $("input[name='h_order_number']").val(),
            'h_pocket_number': $("input[name='h_pocket_number']").val(),
            'h_buyer': $("input[name='h_buyer']").val(),
            'h_title': $("input[name='h_title']").val(),
            'h_barcode': $("input[name='h_barcode']").val(),
            'h_stock_code': $("input[name='h_stock_code']").val(),
            'h_color': $("input[name='h_color']").val(),
            'h_size': $("input[name='h_size']").val(),
            'h_quantity': $("input[name='h_quantity']").val(),
            'h_unit_price': $("input[name='h_unit_price']").val(),
            'h_sales_price': $("input[name='h_sales_price']").val(),
            'h_discount_price': $("input[name='h_discount_price']").val(),
            'h_city': $("input[name='h_city']").val(),
            'h_order_date': $("input[name='h_order_date']").val(),
            'h_status': $("select[name='h_status']").val(),
        },
        dataType: 'json',
        beforeSend: function () {
        },
        success: function (data) {
            if (data === 'success') {
                swal('Hepsiburada Siparişi Eklendi', '', 'success');
                setTimeout(function () {
                    window.location.reload()
                }, 2000)
            }else{
                swal('Bir Hata Meydana Geldi', 'Doldurulması gereken alanlar doğru şekilde doldurulmamış olabilir.', 'error');
            }

        },
        error: function (e) {
            iziToast.error({
                title: 'Hata !',
                message: `Bir hata meydana geldi. ${e}.`,
                position: 'topRight'
            });
        }
    });

})
