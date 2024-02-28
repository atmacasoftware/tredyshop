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


        if (_minPrice == '') {
            _minPrice = $("#minPrice").attr("data-value")
        }

        if (_maxPrice == '') {
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

        $("#dropdownFilterBtn .text").text($("input[name='arrangement']:checked").attr('data-name'))

        if (search.length > 0) {
            _filterObj.keyword = search

            $.ajax({
                url: `/filter/searching/`,
                data: _filterObj,
                dataType: 'json',
                beforeSend: function () {
                    $(".product-collection-grid .row").html('')
                },
                success: function (res) {
                    $(".listing-result__body .products-grid-row").html('')
                    $(".listing-result__body .products-grid-row").append(res.data)
                }
            });
        }

        $("#loadMore").attr("filter-color", _filterObj['color'])
        $("#loadMore").attr("filter-sizer", _filterObj['size'])
        $("#loadMore").attr("filter-minprice", _filterObj['minPrice'])
        $("#loadMore").attr("filter-maxprice", _filterObj['maxPrice'])
        $("#loadMore").attr("filter-arrangement", _filterObj['arrangement'])

        if (subcategory != 'None' && subbottomcategory != 'None' && brand === 'None') {
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
                    $(".listing-result__body .products-grid-row").html('')
                    $(".listing-result__body .products-grid-row").append(res.data)
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
                $("#loadMore").attr('disabled','disabled')
                $("#loadMore").html(`
                    <div class="spinner-border text-white" role="status">
  <span class="visually-hidden">Loading...</span>
</div>
                `)
            },
            success: function (res) {
                 $("#loadMore").attr('disabled','disabled')
                $("#loadMore").html(`
                    <div class="spinner-border text-white" role="status">
  <span class="visually-hidden">Loading...</span>
</div>
                `)

                setTimeout(function () {
                    $(".listing-result__body .products-grid-row").append(res.data)
                    $("#loadMore").removeAttr('disabled','disabled')
                    $("#loadMore").html(`
                    <span class="icon">
                                                        <svg xmlns="https://www.w3.org/2000/svg" width="24" height="24"
                                                             viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                                             stroke-width="2" stroke-linecap="round"
                                                             stroke-linejoin="round" class="feather feather-arrow-down">
                                                            <line x1="12" y1="5" x2="12" y2="19"></line>
                                                            <polyline points="19 12 12 19 5 12"></polyline>
                                                        </svg>
                                                    </span>
                                                    <span class="text">
                                                        Daha Fazla Yükle
                                                    </span>
                `)
                }, 2000)

                var _totalShowing = $(".product-item").length;
                if (_totalShowing == _total) {
                    $("#loadMore").hide()
                }

            }
        })
    });
});