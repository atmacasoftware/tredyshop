const emailInput = document.getElementById("email");

$(document).ready(function () {
    $(".warning").hide()
    emailInput.addEventListener('change', e => {
        const email = e.target.value

        $.ajax({
            url: '/check-email/',
            type: 'GET',
            data: {
                'email': email,
                'csrfmiddlewaretoken': '{{ csrf_token }}',
            },
            success: function (data) {
                if (data.is_taken) {
                    $(".warning").show()
                    $("#register_btn").attr('disabled', 'disabled');
                } else {
                    $("#register_btn").removeAttr('disabled', 'disabled')
                    $(".warning").hide()
                }
            },
            error: function (error) {
            }
        })
    })
})




