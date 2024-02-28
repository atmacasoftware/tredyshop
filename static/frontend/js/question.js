$(document).ready(function () {

    const productID = document.getElementById("product_id").value

    $("#loadMore").on('click', function (e) {
        e.preventDefault();
        var _currentProducts = $(".reviews__list-item").length;
        var _limit = $(this).attr("data-limit");
        var _max = $(this).attr("data-max");
        console.log(_limit)
        console.log(_max)
        if (_currentProducts >= _max) {
            $(this).hide();
        } else {
            $.ajax({
                type: 'GET',
                url: `/urun/${productID}/urun-sorulari/daha-fazla-yukle/`,
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