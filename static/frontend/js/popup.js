$(document).ready(function () {
    const showBtns = document.querySelectorAll('.popup-show');

    showBtns.forEach((btn) => {
        btn.addEventListener('click', function (e) {
            var target = btn.getAttribute("data-popup-target")

            if (target) {
                var popup = document.getElementById(`${target}`);
                popup.style.display = 'block'
                popup.style.visibility = 'visible'

                var closeBtn = document.querySelector(`#${target} .close-btn`)

                closeBtn.addEventListener('click', function () {
                    popup.style.display = 'none'
                    popup.style.visibility = 'hidden'
                });

            }


        })
    });


});