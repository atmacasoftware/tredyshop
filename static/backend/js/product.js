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

    //$(".waiting").hide()

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

    $("#deleteNotActiveProduct").on('click', function () {
        $.ajax({
            url: $(this).attr('data-target'),
            dataType: 'json',
            beforeSend: function () {
                $(".waiting").show()
            },
            success: function (data) {
                $(".waiting").hide()
                if (data === 'success'){
                    window.location.reload()
                }
            }
        });
    });
});
