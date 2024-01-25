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


    $(".filter-checkbox").on('click', function () {

        var _filterObj = {};

        $(".filter-checkbox").each(function (index, ele) {
            var _filterVal = $(this).val();
            var _filterKey = $(this).data('filter');
            _filterObj[_filterKey] = Array.from(document.querySelectorAll('input[data-filter=' + _filterKey + ']:checked')).map(function (el) {
                return el.value;
            });

        });

        $("#doActive").on('click', function () {
            $.ajax({
                url: `/yonetim/trendyol/hatali-urunler/aktif-yap/barcode/ajax/`,
                data: _filterObj,
                dataType: 'json',
                beforeSend: function () {
                    $(".waiting").css('display','flex')
                    $(".waiting").css('visibility','visible')
                },
                success: function (data) {
                    $(".waiting").css('display','none')
                    $(".waiting").css('visibility','hidden')
                    window.location.reload()
                }
            });
        });
    });

});
