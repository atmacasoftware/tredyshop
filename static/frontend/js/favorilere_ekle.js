$(document).ready(function () {
    $("#addFavourite").click(function (e) {
        e.preventDefault();
        $.ajax({
            url: `/favourite/`,
            type: 'GET',
            data: {
                'product_id': $(this).attr("data-id"),
            },
            beforeSend: function () {

            },
            success: function (data) {
                var status = $("#addFavourite").attr('data-result')
                if (status == "not-favourite") {
                    $("#addFavourite").html('')
                    $("#addFavourite").html(`<i class="bi bi-heart-fill"></i>`)
                    $("#addFavourite").attr("data-result", "favourite")
                }else{
                    $("#addFavourite").html('')
                    $("#addFavourite").html(`<svg xmlns="https://www.w3.org/2000/svg" width="24" height="24"
                                             viewBox="0 0 24 24"
                                             fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                             stroke-linejoin="round" class="feather feather-heart">
                                            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                                        </svg>`)
                    $("#addFavourite").attr("data-result", "not-favourite")
                }
            },
            error: function (error) {

            }
        })
    });
});