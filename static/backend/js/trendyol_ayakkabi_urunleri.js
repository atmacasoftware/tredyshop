$(document).ready(function () {
    const allCategoryBtn = document.querySelectorAll('.category-btn');

    allCategoryBtn.forEach((item) => {
        item.addEventListener('click', function () {

            var category_no = $(this).attr('data-category')

            $.ajax({
                url: `/yonetim/trendyol/urun-giris/ayakkabi-urunleri-getir/${category_no}/`,
                dataType: 'json',
                beforeSend: function () {
                    $(".waiting").show()
                },
                success: function (res) {
                    $(".waiting").hide()
                    $(".productTable").html('')
                    $(".productTable").html(res.data)
                }
            });
        })
    })

});