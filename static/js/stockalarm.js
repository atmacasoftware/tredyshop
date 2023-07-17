$(document).ready(function (){
   var product_id = $("#product_id").val()

   $("#stockAlarm").click(function (e){
       e.preventDefault();

       $.ajax({
            url: `/stockalarm`,
            type: 'GET',
            data: {
                'product_id': product_id,
            },
            success: function (data) {
                $("#stockAlarm").attr("disabled","disabled")
            },
            error: function (error) {
               $("#stockAlarm").remove("disabled")
            }
        })

   })

});