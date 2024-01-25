$("#cashPaymentTr").show()
$("#threeInstallmentTr").hide()
$("#sixInstallmentTr").hide()
$("#nineInstallmentTr").hide()
$("#twelveInstallmentTr").hide()
$(".cardnumber_error").hide()
var $cc = {}
$cc.validate = function (e) {

    //if the input is empty reset the indicators to their default classes
    if (e.target.value == '') {
        e.target.nextElementSibling.className = 'card-valid';
        return
    }


    //Retrieve the value of the input and remove all non-number characters
    var number = String(e.target.value);
    var cleanNumber = '';
    for (var i = 0; i < number.length; i++) {
        if (/^[0-9]+$/.test(number.charAt(i))) {
            cleanNumber += number.charAt(i);
        }
    }

    //Only parse and correct the input value if the key pressed isn't backspace.
    if (e.key != 'Backspace') {
        //Format the value to include spaces in the correct locations
        var formatNumber = '';
        for (var i = 0; i < cleanNumber.length; i++) {
            if (i == 3 || i == 7 || i == 11) {
                formatNumber = formatNumber + cleanNumber.charAt(i) + ' '
            } else {
                formatNumber += cleanNumber.charAt(i)
            }
        }
        e.target.value = formatNumber;
    }


    //run the Luhn algorithm on the number if it is at least equal to the shortest card length
    if (cleanNumber.length == 16) {
        var isLuhn = luhn(cleanNumber);
    }


    function luhn(number) {
        var numberArray = number.split('').reverse();
        for (var i = 0; i < numberArray.length; i++) {
            if (i % 2 != 0) {
                numberArray[i] = numberArray[i] * 2;
                if (numberArray[i] > 9) {
                    numberArray[i] = parseInt(String(numberArray[i]).charAt(0)) + parseInt(String(numberArray[i]).charAt(1))
                }
            }
        }
        var sum = 0;
        for (var i = 1; i < numberArray.length; i++) {
            sum += parseInt(numberArray[i]);
        }

        sum = sum * 9 % 10;
        if (numberArray[0] == sum) {
            return true
        } else {
            return false
        }
    }


    //if the number passes the Luhn algorithm add the class 'active'
    if (isLuhn == true) {
        e.target.nextElementSibling.className = 'card-valid active'
        $(".cardnumber_error").hide()
        $("#installmentTableBody").empty();
        let card_nospace_number = $("#cardnumber").val().replaceAll(" ", "")
        $("#paytrCardNumber").val(card_nospace_number)
        let bin_code = parseInt($("#cardnumber").val().replaceAll(" ", "").slice(0, 8))

        $.ajax({
            url: `/checkout`,
            data: {'bin_code': bin_code},
            dataType: 'json',

            success: function (res) {
                $("#kartTipi").val(res[1])
                $("#installmentTableBody").empty();
                for(i=0; i <= 11; i++){
                    var taksit_sayisi = res[0][i]["taksit_sayisi"]
                    var vadeli_fiyat = res[0][i]["vadeli_fiyat"].toFixed(2)

                    $("#installmentTableBody").append(
                        `
                        <tr id="${taksit_sayisi == "Tek Çekim" ? "0"  : taksit_sayisi}InstallmentTr">
                             <td>
                                 <input type="radio"
                                        name="paymentInstallmentCount" required
                                        id="${taksit_sayisi == "Tek Çekim" ? "0"  : taksit_sayisi}Installment" value="${vadeli_fiyat}" data-installment="${taksit_sayisi}">
                                 <label for="${taksit_sayisi == "Tek Çekim" ? "0"  : taksit_sayisi}Installment">${taksit_sayisi == "Tek Çekim" ? 'Tek Çekim': taksit_sayisi + ' Taksit' }</label>
                             </td>
                             <td id="${taksit_sayisi}InstallmentText" class="installmentClass">
                                 ${vadeli_fiyat} TL
                             </td>
                        </tr>
                        `
                    )
                }

                var tek_cekim = parseFloat($("#0Installment").val())

                $('input[name="paymentInstallmentCount"]').change(function() {
                    $("#grandTotal").text($(this).val() + ' TL')
                    $("#orderTotal").val($(this).val())
                    $("#generalTotal2 b").text($(this).val() + ' TL')
                    $("#generalTotal b").text($(this).val() + ' TL')
                    $("#paytrPaymentAmount").val($(this).val())

                    if($(this).attr("data-installment") == "Tek Çekim"){
                        $("#resultInstallmentCount").val("0")
                    }else{
                        $("#resultInstallmentCount").val($(this).attr("data-installment"))
                    }


                    var vade_farki = (parseFloat($(this).val()) - tek_cekim).toFixed(2)
                    $(".maturity_difference1").text(vade_farki + ' TL')
                    $(".maturity_difference2").text(vade_farki + ' TL')
                    $(".maturity_difference3").text(vade_farki + ' TL')
                    $(".maturity_difference4").text(vade_farki + ' TL')
                    $(".paymentTypeAndPlan").text($(this).attr("data-installment") === "Tek Çekim" ? "Peşin Ödeme" : $(this).attr("data-installment") + "Taksit")

                    $("#preliminaryForm").text($(".preliminary_form_body").html())
                    $("#distanceSellingForm").text($(".distance_selling_form_body").html())

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

                    $.ajax({
                        type: "POST",
                        headers: {'X-CSRFToken': csrftoken},
                        url: `/token-olustur`,
                        data: {
                            'user_ip': $("input[name='user_ip']").val(),
                            'merchant_oid': $("input[name='merchant_oid']").val(),
                            'email': $("input[name='email']").val(),
                            'payment_amount': $("input[name='order_total']").val(),
                            'installment_count': $("input[name='installment_count']").val(),
                        },
                        dataType: 'json',
                        success: function (res) {
                            $("input[name='paytr_token']").val(res)
                        }
                    });


                    $.ajax({
                        type: "POST",
                        url: `/sozlesme-onayi`,
                        headers: {'X-CSRFToken': csrftoken},
                        data: {
                            'order_number': $("input[name='merchant_oid']").val(),
                            'preliminary_form': $("textarea[name='preliminary_form']").val(),
                            'distance_selling_contract': $("textarea[name='distance_selling_form']").val(),
                        },
                        dataType: 'json',
                        success: function (res) {

                        }
                    });

                });
            }
        });




    } else {
        e.target.nextElementSibling.className = 'card-valid invalid'
        $(".cardnumber_error").show()
        $("#cardnumber").addClass('invalid')
        $("#installmentTableBody").empty();
    }

    var card_types = [
        {
            name: 'amex',
            pattern: /^3[47]/,
            valid_length: [15]
        }, {
            name: 'diners_club_carte_blanche',
            pattern: /^30[0-5]/,
            valid_length: [14]
        }, {
            name: 'diners_club_international',
            pattern: /^36/,
            valid_length: [14]
        }, {
            name: 'jcb',
            pattern: /^35(2[89]|[3-8][0-9])/,
            valid_length: [16]
        }, {
            name: 'laser',
            pattern: /^(6304|670[69]|6771)/,
            valid_length: [16, 17, 18, 19]
        }, {
            name: 'visa_electron',
            pattern: /^(4026|417500|4508|4844|491(3|7))/,
            valid_length: [16]
        }, {
            name: 'visa',
            pattern: /^4/,
            valid_length: [16]
        }, {
            name: 'mastercard',
            pattern: /^5[1-5]/,
            valid_length: [16]
        }, {
            name: 'maestro',
            pattern: /^(5018|5020|5038|6304|6759|676[1-3])/,
            valid_length: [12, 13, 14, 15, 16, 17, 18, 19]
        }, {
            name: 'discover',
            pattern: /^(6011|622(12[6-9]|1[3-9][0-9]|[2-8][0-9]{2}|9[0-1][0-9]|92[0-5]|64[4-9])|65)/,
            valid_length: [16]
        }
    ];

}



$cc.expiry = function (e) {
    if (e.key != 'Backspace') {
        var number = String(this.value);

        //remove all non-number character from the value
        var cleanNumber = '';
        for (var i = 0; i < number.length; i++) {
            if (i == 1 && number.charAt(i) == '/') {
                cleanNumber = 0 + number.charAt(0);
            }
            if (/^[0-9]+$/.test(number.charAt(i))) {
                cleanNumber += number.charAt(i);
            }
        }

        var formattedMonth = ''
        for (var i = 0; i < cleanNumber.length; i++) {
            if (/^[0-9]+$/.test(cleanNumber.charAt(i))) {
                //if the number is greater than 1 append a zero to force a 2 digit month
                if (i == 0 && cleanNumber.charAt(i) > 1) {
                    formattedMonth += 0;
                    formattedMonth += cleanNumber.charAt(i);
                    formattedMonth += '/';
                }
                //add a '/' after the second number
                else if (i == 1) {
                    formattedMonth += cleanNumber.charAt(i);
                    formattedMonth += '/';
                }
                //force a 4 digit year
                else if (i == 2 && cleanNumber.charAt(i) < 2) {
                    formattedMonth += '20' + cleanNumber.charAt(i);
                } else {
                    formattedMonth += cleanNumber.charAt(i);
                }

            }
        }
        this.value = formattedMonth;
    }
}


$("input[name='cc_owner']").keyup(function (){
    if($(this).val().length < 1){
        $(this).addClass('invalid-form')
    }else{
        if($(this).hasClass('invalid-form')){
            $(this).removeClass('invalid-form')
        }
    }

})

$("input[name='expiry_month']").keyup(function (){

    if (/\D/g.test(this.value))
    {
        // Filter non-digits from input value.
        this.value = this.value.replace(/\D/g, '');
    }

    if($(this).val() > 12 || $(this).val() == 0){
        $(this).addClass('invalid-form')
    }else{
        if($(this).hasClass('invalid-form')){
            $(this).removeClass('invalid-form')
        }
    }

})

$("input[name='cvv']").keyup(function (){

    if (/\D/g.test(this.value))
    {
        // Filter non-digits from input value.
        this.value = this.value.replace(/\D/g, '');
    }

})

$("input[name='expiry_year']").keyup(function (){

    if (/\D/g.test(this.value))
    {
        // Filter non-digits from input value.
        this.value = this.value.replace(/\D/g, '');
    }

    if($(this).val() < 23){
        $(this).addClass('invalid-form')
    }else{
        if($(this).hasClass('invalid-form')){
            $(this).removeClass('invalid-form')
        }
    }

})
