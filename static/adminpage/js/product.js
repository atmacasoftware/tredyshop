$(document).ready(function () {

    $("tbody tr").click(function () {
        $(this).addClass("selected").siblings().removeClass("selected");
    })

    $('#selectAllRow').click(function (event) {

        var selected = this.checked;
        // Iterate each checkbox
        $(':checkbox').each(function () {
            this.checked = selected;
        });

    });

    $(".waiting").hide()

    $(".filter-checkbox").on('click', function () {

        var _filterObj = {};


        $(".filter-checkbox").each(function (index, ele) {
            var _filterVal = $(this).val();
            var _filterKey = $(this).data('filter');
            _filterObj[_filterKey] = Array.from(document.querySelectorAll('input[data-filter=' + _filterKey + ']:checked')).map(function (el) {
                return el.value;
            });


        });

        $("#deletingSelect").on('click', function () {
            $.ajax({
                url: `/yonetim/urunler/sil/json/`,
                data: _filterObj,
                dataType: 'json',
                beforeSend: function () {
                    $(".waiting").show()
                },
                success: function (data) {
                    $(".waiting").hide()
                    location.reload();
                }
            });
        });
    });

    //$(".filter-checkbox").on('click', function () {
//
    //    var _filterObj = {};
//
    //    $(".filter-checkbox").each(function (index, ele) {
    //        var _filterVal = $(this).val();
//
    //        var _filterKey = $(this).data('filter');
    //        _filterObj[_filterKey] = Array.from(document.querySelectorAll('input[data-filter=' + _filterKey + ']:checked')).map(function (el) {
    //            return el.value;
    //        });
//
    //    });
//
    //    $("#loadMore").attr("data-filter-desc", _filterObj['desc'])
//
    //    $.ajax({
    //        url: `/yonetim/urunler/json/`,
    //        data: _filterObj,
    //        dataType: 'json',
//
    //        success: function (res) {
    //            console.log(res.data)
    //            $("tbody").html('')
    //            $("tbody").append(res.data)
    //        },
//
    //    });
//
//
    //});
//
    //$("#loadMore").on('click', function () {
    //    var _currentProducts = $("tbody tr").length;
    //    var _page = $(this).attr("data-page");
    //    var _total = $(this).attr("data-total");
//
//
    //    $.ajax({
    //        url: `/yonetim/urunler/json/yukle/`,
    //        data: {
    //            page: _page,
    //            offset: _currentProducts,
    //            desc: $("#loadMore").attr('data-filter-desc').split(','),
    //        },
    //        dataType: 'json',
    //        success: function (res) {
    //            var previous_page = parseInt(_page)
    //            var current_page = previous_page + 1
    //            console.log(current_page)
    //            $("tbody").html('')
    //            $("tbody").append(res.data)
    //            $("#loadMore").attr("data-page", current_page)
    //            $(".current__page").text(current_page)
//
    //            if (current_page == _total) {
    //                $("#loadMore").attr("disabled", true)
    //            }
//
    //        }
    //    })
//
    //});
});
