$(document).ready(function () {

    var category = $("#data-category").val();
    var subcategory = $("#data-subcategory").val();
    var subbottomcategory = $("#data-bottomcategory").val();
    var brand = $("#data-brands").val();
    var search = $("#data-search").val()

    $(".filter-checkbox, #priceFilterBtn").on('click', function () {

        var _filterObj = {};
        var _minPrice = $("#minPrice").val()
        var _maxPrice = $("#maxPrice").val()

        if (_minPrice == ''){
            _minPrice = $("#minPrice").attr("data-value")
        }

        if (_maxPrice == ''){
            _maxPrice = $("#maxPrice").attr("data-value")
        }

        _filterObj.minPrice = _minPrice
        _filterObj.maxPrice = _maxPrice
        $(".filter-checkbox").each(function (index, ele) {
            var _filterVal = $(this).val();
            var _filterKey = $(this).data('filter');
            _filterObj[_filterKey] = Array.from(document.querySelectorAll('input[data-filter=' + _filterKey + ']:checked')).map(function (el) {
                return el.value;
            });


        });

        if(search.length > 0){
            _filterObj.keyword = search

            $.ajax({
                url: `/filter/searching/`,
                data: _filterObj,
                dataType: 'json',
                beforeSend: function () {
                    $(".product-collection-grid .row").html('')
                },
                success: function (res) {
                    $(".product-collection-grid .row").html('')
                    $(".product-collection-grid .row").append(res.data)
                }
            });
        }

        $("#loadMore").attr("filter-color",_filterObj['color'])
        $("#loadMore").attr("filter-sizer",_filterObj['size'])
        $("#loadMore").attr("filter-minprice",_filterObj['minPrice'])
        $("#loadMore").attr("filter-maxprice",_filterObj['maxPrice'])
        $("#loadMore").attr("filter-arrangement",_filterObj['arrangement'])


        if (subcategory != 'None' && subbottomcategory === 'None' && brand === 'None') {
            $.ajax({
                url: `/filtreler/${category}/${subcategory}`,
                data: _filterObj,
                dataType: 'json',
                beforeSend: function () {
                    $(".product_loader").show()
                    $(".product-collection-grid .row").html('')
                },
                success: function (res) {
                    $(".product_loader").hide()
                    $(".product-collection-grid .row").html('')
                    $(".product-collection-grid .row").append(res.data)
                }
            });
        } else if (subcategory != 'None' && subbottomcategory != 'None' && brand === 'None') {
            $.ajax({
                url: `/filtreler/${category}/${subcategory}/${subbottomcategory}`,
                data: _filterObj,
                dataType: 'json',
                beforeSend: function () {
                    $(".product_loader").show()
                    $(".product-collection-grid .row").html('')
                },
                success: function (res) {
                    $(".product_loader").hide()
                    $(".product-collection-grid .row").html('')
                    $(".product-collection-grid .row").append(res.data)
                }
            });
        } else if (subcategory.length == 'None' && subbottomcategory == 'None' && brand.length != 'None') {
            $.ajax({
                url: `/filtreler/marka/${brand}`,
                data: _filterObj,
                dataType: 'json',
                beforeSend: function () {
                    $(".product_loader").show()
                    $(".product-collection-grid .row").html('')
                },
                success: function (res) {
                    $(".product_loader").hide()
                    $(".product-collection-grid .row").append(res.data)
                }
            });
        }
    });

    $(".product_loader").hide()

    $("#loadMore").on('click', function () {
        var _currentProducts = $(".product-item").length;
        var _limit = $(this).attr("data-limit");
        var _total = $(this).attr("data-total");
        var _category = $(this).attr("data-category");
        var _subcategory = $(this).attr("data-subcategory");
        var _bottmcategory = $(this).attr("data-bottomcategory");
        var _brands = $(this).attr("data-brands");

        console.log($("#loadMore").attr("filter-arrangement"))

        $.ajax({
            url: '/load-more-product/',
            data: {
                limit: _limit,
                offset: _currentProducts,
                category: _category,
                subcategory: _subcategory,
                subbottomcategory: _bottmcategory,
                brands: _brands,
                color: $("#loadMore").attr('filter-color').split(','),
                sizes: $("#loadMore").attr('filter-sizer').split(','),
                minPrice: $("#loadMore").attr("filter-minprice"),
                maxPrice: $("#loadMore").attr("filter-maxprice"),
                arrangement: $("#loadMore").attr("filter-arrangement"),
            },
            dataType: 'json',
            beforeSend: function () {
                $("#loadMore").hide()
                $(".product_loader").show()

            },
            success: function (res) {
                $(".product_loader").hide()
                $(".product-collection-grid .row").append(res.data)
                $("#loadMore").show()

                var _totalShowing = $(".product-item").length;
                if(_totalShowing == _total){
                    $("#loadMore").hide()
                }

            }
        })
    });
});