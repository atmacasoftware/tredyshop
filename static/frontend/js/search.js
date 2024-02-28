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
                        `<li style="background: none;">
                                <div class="search-div" style="display: flex; justify-content: center; align-items: center; flex-direction: column; width: 100%; height: 300px;">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
  <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
</svg>
                                    <p style="margin-top: 5px;">Aradığınız kelimede ürün bulamadım.</p>
                                    
                                </div>
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
        if (e.target.value.length > 2) {
            $(".back-dard").css("display", "block")
            $(".search-result-box").css("display", "block")
            sendSearchData(e.target.value)
        } else {
            $(".back-dard").css("display", "none")
            $(".search-result-box").css("display", "none")
        }
    })

    window.onclick = function (event){
        if(!event.target.matches(".search-div")){
            $(".back-dard").css("display", "none")
            $(".search-result-box").css("display", "none")
        }
    }
});