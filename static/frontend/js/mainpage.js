$(document).ready(function () {
    const baseUrl = "https://www.tredyshop.com"

    $.ajax({
        url: `${baseUrl}/apits/en-cok-satilan/`,
        dataType: 'json',
        beforeSend: function () {

        },
        success: function (res) {
            var data = res.data
            var wrapper = document.querySelector(".onerilen-urunler")
            wrapper.innerHTML = ''
            data.forEach((item) => {
                wrapper.innerHTML += `
                <div class="col-xxl-2 col-xl-3 col-lg-3 col-md-4 col-6 grid-item-col">
                            <div class="grid-item">
                                <div class="product-grid-item">
                                    <div class="product">
                                        <a class="a-block" href="${baseUrl}/urun/${item.slug}">
                                            <div class="product__image">
                                                <img src="${item.image_url1}" alt="IMG" width="400" height="400">
                                            </div>
                                        </a>
                                        <div class="product__description">
                                            <a class="a-block" href="https://www.tredyshop.com/urun/${item.slug}">
                                                <div class="product_prices">
                                                            ${item.is_discountprice == "True" ? `<b>${item.discountprice} TL</b>` : `<b>${item.price} TL</b>`}
                                                            ${item.is_discountprice == "False" ? `<b>${item.price} TL TL</b>` : ''}
                                      
                                                </div>
                                            </a>
                                            <div class="product_name">
                                               <a href="https://www.tredyshop.com/urun/${item.slug}">
                                                  ${item.title}
                                               </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                `
            })

        }
    });
    $.ajax({
        url: 'https://www.tredyshop.com/apits/new-product/',
        dataType: 'json',
        beforeSend: function () {

        },
        success: function (res) {
            var data = res.data
            var wrapper = document.querySelector(".trend-urunler")
            wrapper.innerHTML = ''
            data.forEach((item) => {
                wrapper.innerHTML += `
                <div class="col-xxl-2 col-xl-3 col-lg-3 col-md-4 col-6 grid-item-col">
                            <div class="grid-item">
                                <div class="product-grid-item">
                                    <div class="product">
                                        <a class="a-block" href="${baseUrl}/urun/${item.slug}">
                                            <div class="product__image">
                                                <img src="${item.image_url1}" alt="IMG" width="400" height="400">
                                            </div>
                                        </a>
                                        <div class="product__description">
                                            <a class="a-block" href="https://www.tredyshop.com/urun/${item.slug}">
                                                <div class="product_prices">
                                                            ${item.is_discountprice == "True" ? `<b>${item.discountprice} TL</b>` : `<b>${item.price} TL</b>`}
                                                            ${item.is_discountprice == "False" ? `<b>${item.price} TL TL</b>` : ''}
                                      
                                                </div>
                                            </a>
                                            <div class="product_name">
                                               <a href="https://www.tredyshop.com/urun/${item.slug}">
                                                  ${item.title}
                                               </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                `
            })

        }
    });
    $.ajax({
        url: 'https://www.tredyshop.com/apits/en-begenilenler/',
        dataType: 'json',
        beforeSend: function () {

        },
        success: function (res) {
            var data = res.data
            var wrapper = document.querySelector(".en-begenilenler")
            wrapper.innerHTML = ''
            data.forEach((item) => {
                wrapper.innerHTML += `
                <div class="col-xxl-2 col-xl-3 col-lg-3 col-md-4 col-6 grid-item-col">
                            <div class="grid-item">
                                <div class="product-grid-item">
                                    <div class="product">
                                        <a class="a-block" href="${baseUrl}/urun/${item.slug}">
                                            <div class="product__image">
                                                <img src="${item.image_url1}" alt="IMG" width="400" height="400">
                                            </div>
                                        </a>
                                        <div class="product__description">
                                            <a class="a-block" href="https://www.tredyshop.com/urun/${item.slug}">
                                                <div class="product_prices">
                                                            ${item.is_discountprice == "True" ? `<b>${item.discountprice} TL</b>` : `<b>${item.price} TL</b>`}
                                                            ${item.is_discountprice == "False" ? `<b>${item.price} TL TL</b>` : ''}
                                      
                                                </div>
                                            </a>
                                            <div class="product_name">
                                               <a href="https://www.tredyshop.com/urun/${item.slug}">
                                                  ${item.title}
                                               </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                `
            })

        }
    });
})