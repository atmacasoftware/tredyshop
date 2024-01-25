const notificationItemDropdown = document.querySelector('.notifications-items')

function startLiveRefreshBildirim() {
        setInterval(function () {
            $(".notifications-items").empty()
            fetch('/yonetim/bildirim-yenile/').then(function (response) {
                return response.json();
            }).then(function (data) {
                if(data[0] === true){
                    $(".notification-toggle").addClass('beep')
                }
                var notifications = data[1]
                notifications.map((items) => {
                    if (items['n_type'] == "1" ){
                        var item = `<a href="<a href="/yonetim/bildirim-goruntule/bildirim_id=${items['id']}/" data-id = "${items['id']}" class="dropdown-item dropdown-item-unread">
                               <div class="dropdown-item-icon bg-warning text-white">
                                    <i class="fas fa-send"></i>
                                </div>
                                <div class="dropdown-item-desc">
                                    ${items['title']}
                                    <div class="time text-primary">${items['passing_time']}</div>
                                </div>
                            </a>`
                    }
                    else if (items['n_type'] == "2" ){
                        var item = `<a href="<a href="/yonetim/bildirim-goruntule/bildirim_id=${items['id']}/" data-id = "${items['id']}" class="dropdown-item dropdown-item-unread">
                               <div class="dropdown-item-icon bg-primary text-white">
                                    <i class="fas fa-check"></i>
                                </div>
                                <div class="dropdown-item-desc">
                                    ${items['title']}
                                    <div class="time text-primary">${items['passing_time']}</div>
                                </div>
                            </a>`
                    }
                    else if (items['n_type'] == "3" ){
                        var item = `<a href="<a href="/yonetim/bildirim-goruntule/bildirim_id=${items['id']}/" data-id = "${items['id']}" class="dropdown-item dropdown-item-unread">
                               <div class="dropdown-item-icon bg-secondary text-white">
                                    <i class="fas fa-cubes-stacked"></i>
                                </div>
                                <div class="dropdown-item-desc">
                                    ${items['title']}
                                    <div class="time text-primary">${items['passing_time']}</div>
                                </div>
                            </a>`
                    }
                    else if (items['n_type'] == "4" ){
                        var item = `<a href="<a href="/yonetim/bildirim-goruntule/bildirim_id=${items['id']}/" data-id = "${items['id']}" class="dropdown-item dropdown-item-unread">
                               <div class="dropdown-item-icon bg-success text-white">
                                    <i class="fas fa-box"></i>
                                </div>
                                <div class="dropdown-item-desc">
                                    ${items['title']}
                                    <div class="time text-primary">${items['passing_time']}</div>
                                </div>
                            </a>`
                    }
                    else if (items['n_type'] == "5" ){
                        var item = `<a href="/yonetim/bildirim-goruntule/bildirim_id=${items['id']}/" data-id = "${items['id']}" class="dropdown-item dropdown-item-unread">
                               <div class="dropdown-item-icon bg-info text-white">
                                    <i class="fas fa-question"></i>
                                </div>
                                <div class="dropdown-item-desc">
                                    ${items['title']}
                                    <div class="time text-primary">${items['passing_time']}</div>
                                </div>
                            </a>`
                    }
                    else if (items['n_type'] == "6" ){
                        var item = `<a href="/yonetim/bildirim-goruntule/bildirim_id=${items['id']}/" data-id = "${items['id']}" class="dropdown-item dropdown-item-unread">
                               <div class="dropdown-item-icon bg-info text-white">
                                    <i class="fas fa-rotate-left"></i>
                                </div>
                                <div class="dropdown-item-desc">
                                    ${items['title']}
                                    <div class="time text-primary">${items['passing_time']}</div>
                                </div>
                            </a>`
                    }
                    else if (items['n_type'] == "7" ){
                        var item = `<a href="/yonetim/bildirim-goruntule/bildirim_id=${items['id']}/" data-id = "${items['id']}" class="dropdown-item dropdown-item-unread">
                               <div class="dropdown-item-icon bg-danger text-white">
                                    <i class="fas fa-comment"></i>
                                </div>
                                <div class="dropdown-item-desc">
                                    ${items['title']}
                                    <div class="time text-primary">${items['passing_time']}</div>
                                </div>
                            </a>`
                    }
                    else{
                        var item = `<a href="/yonetim/bildirim-goruntule/bildirim_id=${items['id']}/" data-id = "${items['id']}" class="dropdown-item dropdown-item-unread">
                               <div class="dropdown-item-icon bg-dark text-white">
                                    <i class="fas fa-user-plus"></i>
                                </div>
                                <div class="dropdown-item-desc">
                                    ${items['title']}
                                    <div class="time text-primary">${items['passing_time']}</div>
                                </div>
                            </a>`
                    }
                   $(".notifications-items").append(item)

                })
            }).catch(function (error) {
                console.log(error)
            });
        }, 60000);
    }

document.addEventListener('DOMContentLoaded', function () {
    startLiveRefreshBildirim();
})

$(document).ready(function () {

    const allReadNotificationBtn = document.getElementById("allReadBtn")
    allReadNotificationBtn.addEventListener('click', function (e) {
        e.preventDefault();
        $.ajax({
            type: 'GET',
            url: '/yonetim/tum-bildirimleri-okundu-olarak-isaretle/',
            beforeSend: function () {
                $(".waiting").css('display', 'flex')
                $(".waiting").css('visibility', 'visible')
            },
            success: (res) => {
                $(".waiting").css('display', 'none')
                $(".waiting").css('visibility', 'hidden')
                window.location.reload()
            }
        })
    })


});