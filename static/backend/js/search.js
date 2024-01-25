$(document).ready(function () {
    const search_form = document.getElementById("generalSearchForm")
    const search_input = document.getElementById("generalSearch")
    const result_box = document.querySelector('.search-result')


    const sendSearchData = (series) => {
        $.ajax({
            type: 'GET',
            url: '/yonetim/arama/',
            data: {
                'series': series,
            },
            beforeSend: function () {
                result_box.classList.add('loading')
                result_box.innerHTML = `<div class="spinner-border text-danger" role="status">
  <span class="visually-hidden">Loading...</span>
</div>`
            },
            success: (res) => {
                result_box.classList.remove('loading')
                const data = res.data
                if (Array.isArray(data)) {
                    result_box.innerHTML = ''
                    data.forEach(series => {
                        result_box.innerHTML += `
                        <div class="search-item">
                <a href="/yonetim/urunler/urun_id=${series.id}/">
                  <img class="mr-3 rounded" width="30" src="${series.image}" alt="product">
                  ${series.p_title}
                </a>
              </div>
                    `
                    })
                } else {
                    if (search_input.value.length > 5) {
                        result_box.innerHTML = `<b>${data}</b>`
                    } else {
                        result_box.classList.add('not-visible')
                    }
                }
            },
            error: (err) => {
                console.log(err)
            }
        })
    }
    search_input.addEventListener('keyup', e => {
        if (e.target.value.length > 5) {
            sendSearchData(e.target.value)
        }
    })

});



