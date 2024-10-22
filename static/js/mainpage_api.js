$(document).ready(function () {

    var baseUrl = 'http://127.0.0.1:8000'

    const allBannerCards = document.querySelectorAll('.banner-card')

    allBannerCards.forEach((item) => {
        item.addEventListener('click', function (e) {
            e.preventDefault();
            var target = item.querySelector('.banner-href').getAttribute('href');
            var banner_id = item.querySelector('.banner-href').getAttribute('data-banner-id');

            $.ajax({
                url: `/yonetim/sayfalar/banner/secili-banner/id=${banner_id}/goruntulenme-yukselt/`,
                dataType: 'json',
                success: function (res) {
                    if (res === 'success'){
                        window.location.href = target
                    }
                }
            });

        })
    })

    $.ajax({
        url: `${baseUrl}/apits/super-firsatlar/`,
        dataType: 'json',
        beforeSend: function () {
            $(".flash_deals_skeleton").show()
        },
        success: function (res) {
            $(".flash_deals_skeleton").hide()
            var data = res.data
            $(".js-owl-cate2").html('')
            data.forEach(function (item, index) {
                $(".js-owl-cate2").append(
                    `
                    <div class="product-countd pd-bd product-inner">
                    <div class="product-item-countd">
                        <div class="product-head product-img">
                            <a href="/urun/${item.get_product_slug}"><img src="${item.kapak}" alt="Product"
                                                           class="flash-deals-image"></a>
                            <div class="ribbon-price v3 red"><span>- ${parseInt(100 - ((parseFloat(item.get_product_discountprice) * 100) / parseFloat(item.get_product_price)))}% </span></div>
                        </div>
                        <div class="product-info">
                            <p class="product-cate text-center">${item.third_category}</p>
                            <div class="product-price thin-price v3">
                                <span class="red">${item.get_product_discountprice} TL</span>
                                <span class="old">${item.get_product_price}</span>
                            </div>
                            <h3 class="product-title text-center v2"><a href="/urun/${item.get_product_slug}">${item.get_product_title}</a></h3>

                        </div>
                    </div>
                </div>
                    `
                )
            });
            $('.js-owl-cate2').owlCarousel({
                margin: 30,
                autoplay: false,
                autoplayTimeout: 10000,
                loop: true,
                dots: true,
                nav: false,
                responsive: {
                    0: {
                        items: 1
                    },
                    480: {
                        items: 2
                    },
                    1024: {
                        items: 3
                    },
                    1200: {
                        items: 3
                    },
                    1600: {
                        items: 3,
                        margin: 40
                    }
                }
            });

        }
    });

    $.ajax({
        url: `${baseUrl}/apits/en-cok-satilan/`,
        dataType: 'json',
        beforeSend: function () {
            $(".most__seller_skeleton").show()
        },
        success: function (res) {
            $(".most__seller_skeleton").hide()
            var data = res.data
            $(".js-owl-product").html('')
            data.forEach(function (item, index) {
                $(".js-owl-product").append(
                    `
                    <div class="product-item">
                <div class="pd-bd product-inner">
                    <div class="product-img">
                        <a href="/urun/${item.get_product_slug}"
                           style="display: flex; justify-content: center; align-items: center;"><img
                                src="${item.kapak}"
                                alt="Product" class="img-reponsive" style="height: 200px; width: auto;"></a>

                    </div>
                    <div class="product-info">
                        <div class="color-group">
                        </div>
                        <div class="element-list element-list-left">
                        </div>
                        <div class="element-list element-list-middle">
                            <p class="product-cate">${item.third_category}</p>
                            <h3 class="product-title"><a href="/urun/${item.get_product_slug}">${item.get_product_title}</a>
                            </h3>
                            <div class="product-bottom">
                                <div class="product-price">
                                    <span>${item.get_product_isdiscount == false ? item.get_product_price : item.get_product_discountprice} TL</span>
                                </div>
                            </div>
                        </div>
                        <div class="product-button-group"
                             style="display: flex; justify-content: center;align-items: center;">
                            <a href="/urun/${item.get_product_slug}" class="btn btn-gradient">Ürünü Gör
                            </a>
                        </div>
                    </div>
                </div>
            </div>
                    `
                )
            })
            $('.js-owl-product').owlCarousel({
                margin: 10,
                autoplay: true,
                autoplayTimeout: 10000,
                loop: true,
                dots: false,
                nav: true,
                navText: ["<span class='fa fa-angle-left'></span>", "<span class='fa fa-angle-right'></span>"],
                responsive: {
                    0: {
                        items: 1
                    },
                    480: {
                        items: 2
                    },
                    1024: {
                        items: 2
                    },
                    1200: {
                        items: 4
                    }
                }
            });

        }
    });

    $.ajax({
        url: `${baseUrl}/apits/ust-giyim-urunleri/`,
        dataType: 'json',
        beforeSend: function () {
            $(".top_wear_skeleton").show()
        },
        success: function (res) {
            $(".top_wear_skeleton").hide()
            var data = res.data

            $(".js-owl-product-top-wear").html('')
            data.forEach(function (item, index) {
                $(".js-owl-product-top-wear").append(
                    `
                    <div class="product-item">
                <div class="pd-bd product-inner">
                    <div class="product-img">
                        <a href="/urun/${item.get_product_slug}"
                           style="display: flex; justify-content: center; align-items: center;"><img
                                src="${item.kapak}"
                                alt="Product" class="img-reponsive" style="height: 200px; width: auto;"></a>

                    </div>
                    <div class="product-info">
                        <div class="color-group">
                        </div>
                        <div class="element-list element-list-left">
                        </div>
                        <div class="element-list element-list-middle">
                            <p class="product-cate">${item.third_category}</p>
                            <h3 class="product-title"><a href="/urun/${item.get_product_slug}">${item.get_product_title}</a>
                            </h3>
                            <div class="product-bottom">
                                <div class="product-price">
                                    <span>${item.get_product_isdiscount == false ? item.get_product_price : item.get_product_discountprice} TL</span>
                                </div>
                            </div>
                        </div>
                        <div class="product-button-group"
                             style="display: flex; justify-content: center;align-items: center;">
                            <a href="/urun/${item.get_product_slug}" class="btn btn-gradient">Ürünü Gör
                            </a>
                        </div>
                    </div>
                </div>
            </div>
                    `
                )
            })
            $('.js-owl-product-top-wear').owlCarousel({
                margin: 10,
                autoplay: true,
                autoplayTimeout: 10000,
                loop: true,
                dots: false,
                nav: true,
                navText: ["<span class='fa fa-angle-left'></span>", "<span class='fa fa-angle-right'></span>"],
                responsive: {
                    0: {
                        items: 1
                    },
                    480: {
                        items: 2
                    },
                    1024: {
                        items: 2
                    },
                    1200: {
                        items: 4
                    }
                }
            });

        }, error: function (e) {
            console.log(e)
        }
    });

    $.ajax({
        url: `${baseUrl}/apits/alt-giyim-urunleri/`,
        dataType: 'json',
        beforeSend: function () {
            $(".bottom_wear_skeleton").show()
        },
        success: function (res) {
            $(".bottom_wear_skeleton").hide()
            var data = res.data

            $(".js-owl-product-bottom-wear").html('')
            data.forEach(function (item, index) {
                $(".js-owl-product-bottom-wear").append(
                    `
                    <div class="product-item">
                <div class="pd-bd product-inner">
                    <div class="product-img">
                        <a href="/urun/${item.get_product_slug}"
                           style="display: flex; justify-content: center; align-items: center;"><img
                                src="${item.kapak}"
                                alt="Product" class="img-reponsive" style="height: 200px; width: auto;"></a>

                    </div>
                    <div class="product-info">
                        <div class="color-group">
                        </div>
                        <div class="element-list element-list-left">
                        </div>
                        <div class="element-list element-list-middle">
                            <p class="product-cate">${item.third_category}</p>
                            <h3 class="product-title"><a href="/urun/${item.get_product_slug}">${item.get_product_title}</a>
                            </h3>
                            <div class="product-bottom">
                                <div class="product-price">
                                    <span>${item.get_product_isdiscount == false ? item.get_product_price : item.get_product_discountprice} TL</span>
                                </div>
                            </div>
                        </div>
                        <div class="product-button-group"
                             style="display: flex; justify-content: center;align-items: center;">
                            <a href="/urun/${item.get_product_slug}" class="btn btn-gradient">Ürünü Gör
                            </a>
                        </div>
                    </div>
                </div>
            </div>
                    `
                )
            })
            $('.js-owl-product-bottom-wear').owlCarousel({
                margin: 10,
                autoplay: true,
                autoplayTimeout: 10000,
                loop: true,
                dots: false,
                nav: true,
                navText: ["<span class='fa fa-angle-left'></span>", "<span class='fa fa-angle-right'></span>"],
                responsive: {
                    0: {
                        items: 1
                    },
                    480: {
                        items: 2
                    },
                    1024: {
                        items: 2
                    },
                    1200: {
                        items: 4
                    }
                }
            });

        }
    });

    $.ajax({
        url: `${baseUrl}/apits/elbise-urunleri/`,
        dataType: 'json',
        beforeSend: function () {
            $(".dress_skeleton").show()
        },
        success: function (res) {
            $(".dress_skeleton").hide()
            var data = res.data
            $(".js-owl-product-dress").html('')
            data.forEach(function (item, index) {
                $(".js-owl-product-dress").append(
                    `
                    <div class="product-item">
                <div class="pd-bd product-inner">
                    <div class="product-img">
                        <a href="/urun/${item.get_product_slug}"
                           style="display: flex; justify-content: center; align-items: center;"><img
                                src="${item.kapak}"
                                alt="Product" class="img-reponsive" style="height: 200px; width: auto;"></a>

                    </div>
                    <div class="product-info">
                        <div class="color-group">
                        </div>
                        <div class="element-list element-list-left">
                        </div>
                        <div class="element-list element-list-middle">
                            <p class="product-cate">${item.third_category}</p>
                            <h3 class="product-title"><a href="/urun/${item.get_product_slug}">${item.get_product_title}</a>
                            </h3>
                            <div class="product-bottom">
                                <div class="product-price">
                                    <span>${item.get_product_isdiscount == false ? item.get_product_price : item.get_product_discountprice} TL</span>
                                </div>
                            </div>
                        </div>
                        <div class="product-button-group"
                             style="display: flex; justify-content: center;align-items: center;">
                            <a href="/urun/${item.get_product_slug}" class="btn btn-gradient">Ürünü Gör
                            </a>
                        </div>
                    </div>
                </div>
            </div>
                    `
                )
            })
            $('.js-owl-product-dress').owlCarousel({
                margin: 10,
                autoplay: true,
                autoplayTimeout: 10000,
                loop: true,
                dots: false,
                nav: true,
                navText: ["<span class='fa fa-angle-left'></span>", "<span class='fa fa-angle-right'></span>"],
                responsive: {
                    0: {
                        items: 1
                    },
                    480: {
                        items: 2
                    },
                    1024: {
                        items: 2
                    },
                    1200: {
                        items: 4
                    }
                }
            });
        }
    });

    $.ajax({
        url: `${baseUrl}/apits/ayakkabi-urunleri/`,
        dataType: 'json',
        beforeSend: function () {
            $(".shoes_skeleton").show()
        },
        success: function (res) {
            $(".shoes_skeleton").hide()
            var data = res.data
            $(".js-owl-product-shoes").html('')
            data.forEach(function (item, index) {
                $(".js-owl-product-shoes").append(
                    `
                    <div class="product-item">
                <div class="pd-bd product-inner">
                    <div class="product-img">
                        <a href="/urun/${item.get_product_slug}"
                           style="display: flex; justify-content: center; align-items: center;"><img
                                src="${item.kapak}"
                                alt="Product" class="img-reponsive" style="height: 200px; width: auto;"></a>

                    </div>
                    <div class="product-info">
                        <div class="color-group">
                        </div>
                        <div class="element-list element-list-left">
                        </div>
                        <div class="element-list element-list-middle">
                            <p class="product-cate">${item.third_category}</p>
                            <h3 class="product-title"><a href="/urun/${item.get_product_slug}">${item.get_product_title}</a>
                            </h3>
                            <div class="product-bottom">
                                <div class="product-price">
                                    <span>${item.get_product_isdiscount == false ? item.get_product_price : item.get_product_discountprice} TL</span>
                                </div>
                            </div>
                        </div>
                        <div class="product-button-group"
                             style="display: flex; justify-content: center;align-items: center;">
                            <a href="/urun/${item.get_product_slug}" class="btn btn-gradient">Ürünü Gör
                            </a>
                        </div>
                    </div>
                </div>
            </div>
                    `
                )
            })
            $('.js-owl-product-shoes').owlCarousel({
                margin: 10,
                autoplay: true,
                autoplayTimeout: 10000,
                loop: true,
                dots: false,
                nav: true,
                navText: ["<span class='fa fa-angle-left'></span>", "<span class='fa fa-angle-right'></span>"],
                responsive: {
                    0: {
                        items: 1
                    },
                    480: {
                        items: 2
                    },
                    1024: {
                        items: 2
                    },
                    1200: {
                        items: 4
                    }
                }
            });
        }
    });

    $.ajax({
        url: `${baseUrl}/apits/aksesuar-urunleri/`,
        dataType: 'json',
        beforeSend: function () {
            $(".accessories_skeleton").show()
        },
        success: function (res) {
            $(".accessories_skeleton").hide()
            var data = res.data
            $(".js-owl-product-accessories").html('')
            data.forEach(function (item, index) {
                $(".js-owl-product-accessories").append(
                    `
                    <div class="product-item">
                <div class="pd-bd product-inner">
                    <div class="product-img">
                        <a href="/urun/${item.get_product_slug}"
                           style="display: flex; justify-content: center; align-items: center;"><img
                                src="${item.kapak}"
                                alt="Product" class="img-reponsive" style="height: 200px; width: auto;"></a>

                    </div>
                    <div class="product-info">
                        <div class="color-group">
                        </div>
                        <div class="element-list element-list-left">
                        </div>
                        <div class="element-list element-list-middle">
                            <p class="product-cate">${item.third_category}</p>
                            <h3 class="product-title"><a href="/urun/${item.get_product_slug}">${item.get_product_title}</a>
                            </h3>
                            <div class="product-bottom">
                                <div class="product-price">
                                    <span>${item.get_product_isdiscount == false ? item.get_product_price : item.get_product_discountprice} TL</span>
                                </div>
                            </div>
                        </div>
                        <div class="product-button-group"
                             style="display: flex; justify-content: center;align-items: center;">
                            <a href="/urun/${item.get_product_slug}" class="btn btn-gradient">Ürünü Gör
                            </a>
                        </div>
                    </div>
                </div>
            </div>
                    `
                )
            })
            $('.js-owl-product-accessories').owlCarousel({
                margin: 10,
                autoplay: true,
                autoplayTimeout: 10000,
                loop: true,
                dots: false,
                nav: true,
                navText: ["<span class='fa fa-angle-left'></span>", "<span class='fa fa-angle-right'></span>"],
                responsive: {
                    0: {
                        items: 1
                    },
                    480: {
                        items: 2
                    },
                    1024: {
                        items: 2
                    },
                    1200: {
                        items: 4
                    }
                }
            });
        }
    });

    $.ajax({
        url: `${baseUrl}/apits/ic-giyim-urunleri/`,
        dataType: 'json',
        beforeSend: function () {
            $(".underwear_skeleton").show()
        },
        success: function (res) {
            $(".underwear_skeleton").hide()
            var data = res.data
            $(".js-owl-product-underwear").html('')
            data.forEach(function (item, index) {
                $(".js-owl-product-underwear").append(
                    `
                    <div class="product-item">
                <div class="pd-bd product-inner">
                    <div class="product-img">
                        <a href="/urun/${item.get_product_slug}"
                           style="display: flex; justify-content: center; align-items: center;"><img
                                src="${item.kapak}"
                                alt="Product" class="img-reponsive" style="height: 200px; width: auto;"></a>

                    </div>
                    <div class="product-info">
                        <div class="color-group">
                        </div>
                        <div class="element-list element-list-left">
                        </div>
                        <div class="element-list element-list-middle">
                            <p class="product-cate">${item.third_category}</p>
                            <h3 class="product-title"><a href="/urun/${item.get_product_slug}">${item.get_product_title}</a>
                            </h3>
                            <div class="product-bottom">
                                <div class="product-price">
                                    <span>${item.get_product_isdiscount == false ? item.get_product_price : item.get_product_discountprice} TL</span>
                                </div>
                            </div>
                        </div>
                        <div class="product-button-group"
                             style="display: flex; justify-content: center;align-items: center;">
                            <a href="/urun/${item.get_product_slug}" class="btn btn-gradient">Ürünü Gör
                            </a>
                        </div>
                    </div>
                </div>
            </div>
                    `
                )
            })
            $('.js-owl-product-underwear').owlCarousel({
                margin: 10,
                autoplay: true,
                autoplayTimeout: 10000,
                loop: true,
                dots: false,
                nav: true,
                navText: ["<span class='fa fa-angle-left'></span>", "<span class='fa fa-angle-right'></span>"],
                responsive: {
                    0: {
                        items: 1
                    },
                    480: {
                        items: 2
                    },
                    1024: {
                        items: 2
                    },
                    1200: {
                        items: 4
                    }
                }
            });
        }
    });

    $.ajax({
        url: `${baseUrl}/apits/en-begenilenler/`,
        dataType: 'json',
        beforeSend: function () {
            $(".mostLike_skeleton").show()
        },
        success: function (res) {
            $(".mostLike_skeleton").hide()
            var data = res.data
            $(".js-owl-product-mostLike").html('')
            data.forEach(function (item, index) {
                $(".js-owl-product-mostLike").append(
                    `
                   <div class="product-item">
                <div class="pd-bd product-inner">
                    <div class="product-img">
                        <a href="/urun/${item.get_product_slug}"
                           style="display: flex; justify-content: center; align-items: center;"><img
                                src="${item.kapak}"
                                alt="Product" class="img-reponsive" style="height: 200px; width: auto;"></a>

                    </div>
                    <div class="product-info">
                        <div class="color-group">
                        </div>
                        <div class="element-list element-list-left">
                        </div>
                        <div class="element-list element-list-middle">
                            <p class="product-cate">${item.third_category}</p>
                            <h3 class="product-title"><a href="/urun/${item.get_product_slug}">${item.get_product_title}</a>
                            </h3>
                            <div class="product-bottom">
                                <div class="product-price">
                                    <span>${item.get_product_isdiscount == false ? item.get_product_price : item.get_product_discountprice} TL</span>
                                </div>
                            </div>
                        </div>
                        <div class="product-button-group"
                             style="display: flex; justify-content: center;align-items: center;">
                            <a href="/urun/${item.get_product_slug}" class="btn btn-gradient">Ürünü Gör
                            </a>
                        </div>
                    </div>
                </div>
            </div>
                    `
                )
            })
            $('.js-owl-product-mostLike').owlCarousel({
                margin: 10,
                autoplay: true,
                autoplayTimeout: 10000,
                loop: true,
                dots: false,
                nav: true,
                navText: ["<span class='fa fa-angle-left'></span>", "<span class='fa fa-angle-right'></span>"],
                responsive: {
                    0: {
                        items: 1
                    },
                    480: {
                        items: 2
                    },
                    1024: {
                        items: 2
                    },
                    1200: {
                        items: 4
                    }
                }
            });
        }
    });

    $.ajax({
        url: `${baseUrl}/apits/en-cok-yorumlananlar/`,
        dataType: 'json',
        beforeSend: function () {
            $(".mostComment_skeleton").show()
        },
        success: function (res) {
            $(".mostComment_skeleton").hide()
            var data = res.data
            $(".js-owl-product-mostComment").html('')
            data.forEach(function (item, index) {
                $(".js-owl-product-mostComment").append(
                    `
                    <div class="product-item">
                <div class="pd-bd product-inner">
                    <div class="product-img">
                        <a href="/urun/${item.get_product_slug}"
                           style="display: flex; justify-content: center; align-items: center;"><img
                                src="${item.kapak}"
                                alt="Product" class="img-reponsive" style="height: 200px; width: auto;"></a>

                    </div>
                    <div class="product-info">
                        <div class="color-group">
                        </div>
                        <div class="element-list element-list-left">
                        </div>
                        <div class="element-list element-list-middle">
                            <p class="product-cate">${item.third_category}</p>
                            <h3 class="product-title"><a href="/urun/${item.get_product_slug}">${item.get_product_title}</a>
                            </h3>
                            <div class="product-bottom">
                                <div class="product-price">
                                    <span>${item.get_product_isdiscount == false ? item.get_product_price : item.get_product_discountprice} TL</span>
                                </div>
                            </div>
                        </div>
                        <div class="product-button-group"
                             style="display: flex; justify-content: center;align-items: center;">
                            <a href="/urun/${item.get_product_slug}" class="btn btn-gradient">Ürünü Gör
                            </a>
                        </div>
                    </div>
                </div>
            </div>
                    `
                )
            })
            $('.js-owl-product-mostComment').owlCarousel({
                margin: 10,
                autoplay: true,
                autoplayTimeout: 10000,
                loop: true,
                dots: false,
                nav: true,
                navText: ["<span class='fa fa-angle-left'></span>", "<span class='fa fa-angle-right'></span>"],
                responsive: {
                    0: {
                        items: 1
                    },
                    480: {
                        items: 2
                    },
                    1024: {
                        items: 2
                    },
                    1200: {
                        items: 4
                    }
                }
            });
        }
    });

});