function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

$(document).ready(function () {
    const registerBtn = document.getElementById("register_btn");
    const againBtn = document.getElementById("againBtn")
    var try_controller = 0

    var seconds = 20


    function startTimer(duration, display) {
        var timer = duration
        var isCountioune = false
        const timerInterval = setInterval(function () {

            display.textContent = `Tekrar Gönder (${timer})`

            if (--timer < 0) {
                isCountioune = true
                timer = duration
                display.removeAttribute("disabled")
                clearInterval(timerInterval);
            }
        }, 1000);

    }

    let timerFunction = () => {
        againBtn.innerHTML = `Tekrar Gönder (${seconds})`

        if (seconds === 0) {
            againBtn.removeAttribute('disabled')
        } else if (seconds > 0) {
            seconds = seconds - 1;
        }
    }

    $('.digit-group').find('input').each(function () {
        $(this).attr('maxlength', 1);
        $(this).on('keyup', function (e) {
            var parent = $($(this).parent());

            if (e.keyCode === 8 || e.keyCode === 37) {
                var prev = parent.find('input#' + $(this).data('previous'));

                if (prev.length) {
                    $(prev).select();
                }
            } else if ((e.keyCode >= 48 && e.keyCode <= 57) || (e.keyCode >= 65 && e.keyCode <= 90) || (e.keyCode >= 96 && e.keyCode <= 105) || e.keyCode === 39) {
                var next = parent.find('input#' + $(this).data('next'));

                if (next.length) {
                    $(next).select();
                } else {
                    if (parent.data('autosubmit')) {
                        parent.submit();
                    }
                }
            }
        });
    });


    $(".loader").hide()
    $.ajax({
        type: "GET",
        url: `/kayit-ol`,
        dataType: 'json',
        success: function (res) {
            var otp = res
            registerBtn.addEventListener('click', function (e) {
                var generalController = 0
                var passController = 0;
                e.preventDefault();
                $.ajax({
                    type: "POST",
                    headers: {'X-CSRFToken': csrftoken},
                    url: `/kayit-ol/gonderiliyor/`,
                    data: {
                        'first_name': $("input[name='first_name']").val(),
                        'last_name': $("input[name='last_name']").val(),
                        'email': $("input[name='email']").val(),
                        'mobile': $("input[name='mobile']").val(),
                        'password': $("input[name='password']").val(),
                        'otp': otp,
                    },
                    dataType: 'json',
                    beforeSend: function () {
                        $(".loader").show();
                    },
                    success: function (data) {
                        $(".loader").hide();
                        var first_name = $("input[name='first_name']").val()
                        var last_name = $("input[name='last_name']").val()
                        var email = $("input[name='email']").val()
                        var mobile = $("input[name='mobile']").val()
                        var password = $("input[name='password']").val()


                        var lowerCaseLetters = /[a-z]/g;
                        if (password.match(lowerCaseLetters)) {
                            passController += 1
                        } else {
                            passController -= 1
                        }

                        // Validate capital letters
                        var upperCaseLetters = /[A-Z]/g;
                        if (password.match(upperCaseLetters)) {
                            passController += 1
                        } else {
                            passController -= 1
                        }

                        // Validate numbers
                        var numbers = /[0-9]/g;
                        if (password.match(numbers)) {
                            passController += 1
                        } else {
                            passController -= 1
                        }

                        // Validate length
                        if (password.length >= 8) {
                            passController += 1
                        } else {
                            passController -= 1
                        }


                        if (first_name.length > 1) {
                            generalController += 1
                        } else {
                            generalController -= 1
                            $("input[name='first_name']").css('border-bottom', '3px solid red')
                        }

                        if (last_name.length > 1) {
                            generalController += 1
                        } else {
                            generalController -= 1
                            $("input[name='last_name']").css('border-bottom', '3px solid red')
                        }

                        if (email.length > 1) {
                            generalController += 1
                        } else {
                            generalController -= 1
                            $("input[name='email']").css('border-bottom', '3px solid red')
                        }

                        if (mobile.length === 14) {
                            generalController += 1
                        } else {
                            generalController -= 1
                            $("input[name='mobile']").css('border-bottom', '3px solid red')
                        }

                        if (passController === 4) {
                            generalController += 1
                        } else {
                            generalController -= 1
                            $("input[name='password']").css('border-bottom', '3px solid red')
                        }

                        //setInterval(timerFunction, 1000);
                        var startCountDown = 180,
                            display = document.querySelector('#againBtn');
                        startTimer(startCountDown, display);

                        if (($(".warning").css('display') != 'flex') && generalController === 5) {
                            $(".send-email").show();

                            document.getElementById("confirm-otp").addEventListener('click', function (e) {
                                var input1 = document.getElementById("digit-1").value;
                                var input2 = document.getElementById("digit-2").value;
                                var input3 = document.getElementById("digit-3").value;
                                var input4 = document.getElementById("digit-4").value;
                                var input5 = document.getElementById("digit-5").value;
                                var input6 = document.getElementById("digit-6").value;
                                var getOtp = input1 + input2 + input3 + input4 + input5 + input6

                                if (otp == getOtp) {
                                    $("#errorOtp").html('')
                                    $.ajax({
                                        type: "POST",
                                        headers: {'X-CSRFToken': csrftoken},
                                        url: `/kayit-ol/gonderiliyor/kayit-yapiliyor/`,
                                        data: {
                                            'first_name': $("input[name='first_name']").val(),
                                            'last_name': $("input[name='last_name']").val(),
                                            'email': $("input[name='email']").val(),
                                            'mobile': $("input[name='mobile']").val(),
                                            'password': $("input[name='password']").val(),
                                        },
                                        beforeSend: function () {
                                            $(".loader").show();
                                        },
                                        success: function (result) {
                                            $(".loader").hide();
                                            window.location.href = '/giris-yap'
                                        }
                                    });

                                } else {
                                    $("#errorOtp").html('*Hatalı doğrulama kodu girdiniz.')
                                }
                            });
                        } else {
                            $(".send-email").hide();
                        }
                    }
                });
            })
            againBtn.addEventListener('click', function (e) {
                try_controller = 1
                var generalController = 0
                var passController = 0;
                e.preventDefault();
                $.ajax({
                    type: "POST",
                    headers: {'X-CSRFToken': csrftoken},
                    url: `/kayit-ol/gonderiliyor/`,
                    data: {
                        'first_name': $("input[name='first_name']").val(),
                        'last_name': $("input[name='last_name']").val(),
                        'email': $("input[name='email']").val(),
                        'mobile': $("input[name='mobile']").val(),
                        'password': $("input[name='password']").val(),
                        'otp': otp,
                    },
                    dataType: 'json',
                    beforeSend: function () {
                        $(".loader").show();
                    },
                    success: function (data) {
                        $(".loader").hide();
                        $("#againBtn").attr('disabled', 'disabled')

                        var first_name = $("input[name='first_name']").val()
                        var last_name = $("input[name='last_name']").val()
                        var email = $("input[name='email']").val()
                        var mobile = $("input[name='mobile']").val()
                        var password = $("input[name='password']").val()


                        var lowerCaseLetters = /[a-z]/g;
                        if (password.match(lowerCaseLetters)) {
                            passController += 1
                        } else {
                            passController -= 1
                        }

                        // Validate capital letters
                        var upperCaseLetters = /[A-Z]/g;
                        if (password.match(upperCaseLetters)) {
                            passController += 1
                        } else {
                            passController -= 1
                        }

                        // Validate numbers
                        var numbers = /[0-9]/g;
                        if (password.match(numbers)) {
                            passController += 1
                        } else {
                            passController -= 1
                        }

                        // Validate length
                        if (password.length >= 8) {
                            passController += 1
                        } else {
                            passController -= 1
                        }


                        if (first_name.length > 1) {
                            generalController += 1
                        } else {
                            generalController -= 1
                            $("input[name='first_name']").css('border-bottom', '3px solid red')
                        }

                        if (last_name.length > 1) {
                            generalController += 1
                        } else {
                            generalController -= 1
                            $("input[name='last_name']").css('border-bottom', '3px solid red')
                        }

                        if (email.length > 1) {
                            generalController += 1
                        } else {
                            generalController -= 1
                            $("input[name='email']").css('border-bottom', '3px solid red')
                        }

                        if (mobile.length === 14) {
                            generalController += 1
                        } else {
                            generalController -= 1
                            $("input[name='mobile']").css('border-bottom', '3px solid red')
                        }

                        if (passController === 4) {
                            generalController += 1
                        } else {
                            generalController -= 1
                            $("input[name='password']").css('border-bottom', '3px solid red')
                        }

                        if (($(".warning").css('display') != 'flex') && generalController === 5) {
                            $(".send-email").show();
                            seconds = 180

                            //setInterval(timerFunction, 1000);

                            var startCountDown = 180,
                                display = document.querySelector('#againBtn');
                            startTimer(startCountDown, display);
                            document.getElementById("confirm-otp").addEventListener('click', function (e) {
                                var input1 = document.getElementById("digit-1").value;
                                var input2 = document.getElementById("digit-2").value;
                                var input3 = document.getElementById("digit-3").value;
                                var input4 = document.getElementById("digit-4").value;
                                var input5 = document.getElementById("digit-5").value;
                                var input6 = document.getElementById("digit-6").value;
                                var getOtp = input1 + input2 + input3 + input4 + input5 + input6

                                if (otp == getOtp) {
                                    $("#errorOtp").html('')
                                    $.ajax({
                                        type: "POST",
                                        headers: {'X-CSRFToken': csrftoken},
                                        url: `/kayit-ol/gonderiliyor/kayit-yapiliyor/`,
                                        data: {
                                            'first_name': $("input[name='first_name']").val(),
                                            'last_name': $("input[name='last_name']").val(),
                                            'email': $("input[name='email']").val(),
                                            'mobile': $("input[name='mobile']").val(),
                                            'password': $("input[name='password']").val(),
                                        },
                                        beforeSend: function () {
                                            $(".loader").show();
                                        },
                                        success: function (result) {
                                            $(".loader").hide();
                                            window.location.href = '/giris-yap'
                                        }
                                    });

                                } else {
                                    $("#errorOtp").html('*Hatalı doğrulama kodu girdiniz.')
                                }
                            });
                        } else {
                            $(".send-email").hide();
                        }
                    }
                });
            })

        }
    });
});