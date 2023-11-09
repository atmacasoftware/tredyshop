$(document).ready(function (){
    const boy = $("#id_height");
    const bel = $("#id_waist");

    var initialSubCategory = $("#id_subcategory").val();

    if(initialSubCategory == 5){
        boy.hide();
        bel.hide();
    }

})