$(document).ready(function () {

    const productID = document.getElementById("product_id").value

    $("#filterForm").on('change', function () {
        $.ajax({
            type: 'GET',
            url: `/urun/${productID}/urun-degerlendirmeleri/filtered/`,
            data: {
                'filter': $("select[name='filter']").val(),
            },
            success: (res) => {
                $(".reviews__list").html('')
                $(".reviews__list").append(res.data)
            },
            error: (err) => {
                console.log(err)
            }
        })
    })

    $("#loadMore").on('click', function (e) {
        e.preventDefault();
        var _currentProducts = $(".reviews__list-item").length;
        var _limit = $(this).attr("data-limit");
        var _max = $(this).attr("data-max");

        if (_currentProducts >= _max) {
            $(this).hide();
        } else {
            $.ajax({
                type: 'GET',
                url: `/urun/${productID}/urun-degerlendirmeleri/daha-fazla-yukle/`,
                data: {
                    'filter': $("select[name='filter']").val(),
                    'offset': _currentProducts,
                    'limit': _limit,
                },
                success: (res) => {
                    $(".reviews__list").append(res.data)
                },
                error: (err) => {
                    console.log(err)
                }
            })
        }

    })


})