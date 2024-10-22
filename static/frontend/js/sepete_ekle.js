$(document).ready(function () {
    var product_id = $("#product_id").val()
    var variant_id = $("#generalVariantId").val()
    var quantity = 1
    $(".feedback-alert").hide()

    $("#addCartBtn").click(function (e) {
        var barcode = $("input[name='select_size']:checked").val()

        if (barcode) {
            $(".feedback-alert").hide()
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

            $.ajax({
                url: `/urun_ekle/`,
                headers: {'X-CSRFToken': csrftoken},
                type: 'POST',
                data: {
                    'product_id': product_id,
                    'quantity': quantity,
                    'barcode': $("input[name='select_size']:checked").val()
                },
                beforeSend: function () {
                    $("#addCartBtn").attr("disabled", "disabled")
                    $("#addCartBtn .text").html('')
                    $("#addCartBtn .icon").html('')
                    $("#addCartBtn .text").html(`<div class="spinner-border text-white" role="status">
                <span class="visually-hidden">Loading...</span>
                </div>`)
                },
                success: function (data) {
                    $("#addCartBtn .icon").html(`<i class="bi bi-cart-check"></i>`)
                    $("#addCartBtn .text").html(`Sepete Eklendi!`)
                    $("#addCartBtn").css('background', '#183691')
                    setTimeout(function () {
                        $("#addCartBtn").removeAttr("disabled", "disabled")
                        $("#addCartBtn .icon").html(`<svg xmlns="https://www.w3.org/2000/svg" width="24" height="24"
                                                             viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                                             stroke-width="2" stroke-linecap="round"
                                                             stroke-linejoin="round"
                                                             class="feather feather-shopping-cart">
                                                            <circle cx="9" cy="21" r="1"></circle>
                                                            <circle cx="20" cy="21" r="1"></circle>
                                                            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                                                        </svg>`)
                        $("#addCartBtn .text").html(`Sepete Ekle`)
                        $("#addCartBtn").css('background', '#D31027')
                    }, 3500);

                },
                error: function (error) {

                }
            })
        }else{
            $(".feedback-alert").show()
        }
    });


})
