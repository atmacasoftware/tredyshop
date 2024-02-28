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
                                        <a class="a-block" href="${baseUrl}/urun/${item.get_product_slug}">
                                            <div class="product__image">
                                                <img src="${baseUrl}${item.get_kapak}" alt="IMG" width="400" height="400">
                                            </div>
                                        </a>
                                        <div class="product__description">
                                            <a class="a-block" href="https://www.tredyshop.com/urun/${item.get_product_slug}">
                                                <div class="product_prices">
                                                            ${item.get_product_isdiscount == "True" ? `<b>${item.get_product_discountprice} TL</b>` : `<b>${item.get_product_price} TL</b>`}
                                                            ${item.get_product_isdiscount == "True" ? `<b>${item.get_product_price} TL TL</b>` : ''}
                                      
                                                </div>
                                            </a>
                                            <div class="product_name">
                                               <a href="https://www.tredyshop.com/urun/${item.get_product_slug}">
                                                  ${item.get_product_title}
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
                                        <a class="a-block" href="https://www.tredyshop.com/urun/${item.get_product_slug}">
                                            <div class="product__image">
                                                <img src="${baseUrl}${item.get_kapak}" alt="IMG" width="400" height="400">
                                            </div>
                                        </a>
                                        <div class="product__description">
                                            <a class="a-block" href="https://www.tredyshop.com/urun/${item.get_product_slug}">
                                                <div class="product_prices">
                                                            ${item.get_product_isdiscount == "True" ? `<b>${item.get_product_discountprice} TL</b>` : `<b>${item.get_product_price} TL</b>`}
                                                            ${item.get_product_isdiscount == "True" ? `<b>${item.get_product_price} TL TL</b>` : ''}
                                      
                                                </div>
                                            </a>
                                            <div class="product_name">
                                               <a href="https://www.tredyshop.com/urun/${item.get_product_slug}">
                                                  ${item.get_product_title}
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
                                        <a class="a-block" href="https://www.tredyshop.com/urun/${item.get_product_slug}">
                                            <div class="product__image">
                                                <img src="${baseUrl}${item.get_kapak}" alt="IMG" width="400" height="400">
                                            </div>
                                        </a>
                                        <div class="product__description">
                                            <a class="a-block" href="https://www.tredyshop.com/urun/${item.get_product_slug}">
                                                <div class="product_prices">
                                                            ${item.get_product_isdiscount == "True" ? `<b>${item.get_product_discountprice} TL</b>` : `<b>${item.get_product_price} TL</b>`}
                                                            ${item.get_product_isdiscount == "True" ? `<b>${item.get_product_price} TL TL</b>` : ''}
                                      
                                                </div>
                                            </a>
                                            <div class="product_name">
                                               <a href="https://www.tredyshop.com/urun/${item.get_product_slug}">
                                                  ${item.get_product_title}
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