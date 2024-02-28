let pswrd = document.getElementById('new_password');
let repswrd = document.getElementById('re_password');
let lowerCase = document.getElementById("validation_lower");
let upperCase = document.getElementById("validation_upper");
let digit = document.getElementById("validation_number");
let minLenght = document.getElementById("validation_length");
let pswrdEquality = document.getElementById("validation_equality");
let checkPass = document.getElementById("check_password");
const submitBtn = document.getElementById("changePasswordBtn");

function checkPassword(data) {
    const lower = new RegExp('(?=.*[a-z])')
    const upper = new RegExp('(?=.*[A-Z])')
    const number = new RegExp('(?=.*[0-9])')
    const length = new RegExp('(?=.{8,})')

    if (lower.test(data)) {
        lowerCase.classList.add('isvalid')
    } else {
        lowerCase.classList.remove('isvalid')
    }

    if (upper.test(data)) {
        upperCase.classList.add('isvalid')
    } else {
        upperCase.classList.remove('isvalid')
    }

    if (number.test(data)) {
        digit.classList.add('isvalid')
    } else {
        digit.classList.remove('isvalid')
    }

    if (length.test(data)) {
        minLenght.classList.add('isvalid')
    } else {
        minLenght.classList.remove('isvalid')
    }

    if (pswrd.value === repswrd.value) {
        pswrdEquality.classList.add('isvalid')
    } else {
        pswrdEquality.classList.remove('isvalid')
    }

}


document.getElementById("changePasswordForm").addEventListener('change', function () {
    if (lowerCase.classList.contains('isvalid') && upperCase.classList.contains('isvalid') && digit.classList.contains('isvalid') && minLenght.classList.contains('isvalid') && pswrd.value === repswrd.value) {
        submitBtn.removeAttribute('disabled')
    } else {
        submitBtn.setAttribute('disabled', true)
    }
})
