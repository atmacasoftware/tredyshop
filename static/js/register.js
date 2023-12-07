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

    const psw = document.getElementById("password");
    var letter = document.getElementById("letter");
    var capital = document.getElementById("capital");
    var number = document.getElementById("number");
    var length = document.getElementById("length");

    psw.onfocus = function () {
        document.getElementById("message").style.display = "block";
    }

    psw.onblur = function () {
        document.getElementById("message").style.display = "none";
    }

    psw.onkeyup = function () {
        // Validate lowercase letters
        var lowerCaseLetters = /[a-z]/g;
        if (psw.value.match(lowerCaseLetters)) {
            letter.classList.remove("invalid");
            letter.classList.add("valid");
        } else {
            letter.classList.remove("valid");
            letter.classList.add("invalid");
        }

        // Validate capital letters
        var upperCaseLetters = /[A-Z]/g;
        if (psw.value.match(upperCaseLetters)) {
            capital.classList.remove("invalid");
            capital.classList.add("valid");
        } else {
            capital.classList.remove("valid");
            capital.classList.add("invalid");
        }

        // Validate numbers
        var numbers = /[0-9]/g;
        if (psw.value.match(numbers)) {
            number.classList.remove("invalid");
            number.classList.add("valid");
        } else {
            number.classList.remove("valid");
            number.classList.add("invalid");
        }

        // Validate length
        if (psw.value.length >= 8) {
            length.classList.remove("invalid");
            length.classList.add("valid");
        } else {
            length.classList.remove("valid");
            length.classList.add("invalid");
        }
    }

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
                                            console.log($("input[name='first_name']").val())
                                            console.log($("input[name='last_name']").val())
                                            console.log($("input[name='email']").val())
                                            console.log($("input[name='mobile']").val())
                                            console.log($("input[name='password']").val())
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

                    }, error: function (e) {
                        console.log(e)
                    }
                });
            })
        }
    });

});