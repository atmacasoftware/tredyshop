$(document).ready(function () {

    const bannerForm = document.getElementById("bannerForm")
    const changeForm = document.querySelector(".change-form")


    $("#banner_type").on('change', function (e) {

        changeForm.innerHTML = ''

        changeForm.innerHTML += `
                <div class="form-group">
                                        <label for="bannerTitle">Banner Adı</label>
                                        <input type="text" class="form-control" required id="bannerTitle"
                                               placeholder="Banner Adı Giriniz" name="bannerTitle">
                                    </div>
            `

        changeForm.innerHTML += `<div class="form-group">
                                    <div class="form-group">
                                        <label for="exampleInputFile">Görsel Seç</label>
                                        <div class="input-group">
                                            <div class="custom-file">
                                                <input type="file" required accept="image/*" name="image" class="custom-file-input" id="image">
                                                <label class="custom-file-label" for="image">Görsel Seç</label>
                                            </div>
                                            <div class="input-group-append">
                                                <span class="input-group-text">Upload</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>`

        if ($(this).val() == "Belirli Tutar Altı") {
            changeForm.innerHTML += `
                                <div class="form-group">
                                        <label for="maxPrice">En Yüksek Fiyat</label>
                                        <input type="number" step="any" class="form-control" required id="maxPrice"
                                               placeholder="En Yüksek Fiyat Giriniz" name="maxPrice">
                                </div>
`
        } else if ($(this).val() == "İndirimli Ürünler") {
            changeForm.innerHTML += `
                <div class="form-group">
                                        <label for="discountRate">İndirim Oranı</label>
                                        <input type="number" step="any" class="form-control" required id="discountRate"
                                               placeholder="İndirim Oranı Giriniz" name="discountRate">
                                    </div>
            `
        } else if ($(this).val() == "Kategori Bazlı Ürünler") {
            changeForm.innerHTML += `<div class="form-group">
                <label for="selectCategory">Kategori Seçiniz</label>
                <select class="custom-select" id="selectCategory" name="selectCategory">
                    
                </select>
            </div>
            `

            $.ajax({
                url: '/ajax/subbottomcategory/',
                type: 'GET',
                beforeSend: function () {
                    $(".waiting").show()
                },
                success: function (data) {
                    $(".waiting").hide()

                    document.getElementById("selectCategory").innerHTML += data


                },
                error: function (error) {
                }
            })

        } else if ($(this).val() == "Kampanya Bazlı Ürünler") {
            changeForm.innerHTML += `
                <div class="form-group">
                                        <label for="campaignName">Kampanya Adı</label>
                                        <input type="text" class="form-control" required id="campaignName"
                                               placeholder="Kampanya Adı Giriniz" name="campaignName">
                                    </div>
            `
        }

        changeForm.innerHTML += `<div class="form-group">
                                        <div class="custom-control custom-switch custom-switch-off-danger custom-switch-on-success">
                                            <input type="checkbox" class="custom-control-input" name="isPublish" id="isPublish">
                                            <label class="custom-control-label" for="isPublish">Yayınlansın mı?</label>
                                        </div>
                                    </div>`
        changeForm.innerHTML += `<button type="submit" class="btn btn-primary btn-block" name="addBtn">Ekle</button>`
    })
});