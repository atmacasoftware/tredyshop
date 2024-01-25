$(document).ready(function () {
    $("#addBtn").on('click', function () {
        $.ajax({
            type: 'GET',
            url: $(this).attr('data-href'),
            dataType: 'json',
            beforeSend: function () {
                $("#dataloader").css('display', 'flex')
            },
            success: function (data) {
                $("#dataloader").css('display', 'none')
            }
        });
    })
})