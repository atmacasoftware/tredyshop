$(document).ready(function () {
        const search_form = document.getElementById("generalSearchForm")
        const search_input = document.getElementById("generalSearch")
        const result_box = document.querySelector('.result-box')

        const sendSearchData = (series) => {
            $.ajax({
                type: 'GET',
                url: '/searching/',
                data: {
                    'series': series,
                },
                success: (res) => {
                    const data = res.data
                    if (data === "no-data") {
                        $(".list-product-search").empty()
                        $(".list-product-search").append(
                            `<li>
                                <p>Herhangi bir kayıt bulunamadı.</p>
                            </li>`
                        )
                    }
                    if (Array.isArray(data)) {
                        $(".list-product-search").empty()

                        if (data === "no-data") {
                            $(".list-product-search").empty()
                        }
                        data.forEach(series => {
                            $(".list-product-search").append(
                                `<li>
                                <a class="flex align-center" href="${series.get_url}">
                                    <div class="product-img">
                                        <img src="${series.image}" alt="">
                                    </div>
                                    <h3 class="product-title">${series.title}</h3>
                                </a>
                            </li>`
                            )
                        });
                    }
                }
                ,
                error: (err) => {
                    console.log(err)
                }
            })
        }

        search_input.addEventListener('keyup', e => {
            sendSearchData(e.target.value)
        })

    }
)
;