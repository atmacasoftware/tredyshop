const billType = document.getElementById("id_bill_type")
const tcField = document.getElementById("field-id_tc")
const companyField = document.getElementById("field-id_company_name")
const taxNumber = document.getElementById("field-id_tax_number")
const taxAdministrationInput = document.getElementById("field-id_tax_administration")


$(document).ready(function () {
    tcField.style.display = 'none'
    companyField.style.display = 'none'
    taxNumber.style.display = 'none'
    taxAdministrationInput.style.display = 'none'

    billType.addEventListener('change', function () {
        if (this.value == "Bireysel") {
            tcField.style.display = 'block'
            companyField.style.display = 'none'
            taxNumber.style.display = 'none'
            taxAdministrationInput.style.display = 'none'
            document.getElementById("id_tc").setAttribute("required", "true")
            document.getElementById("id_company_name").removeAttribute("required")
            document.getElementById("id_tax_number").removeAttribute("required")
            document.getElementById("id_tax_administration").removeAttribute("required")

        } else if (this.value == "Kurumsal") {
            tcField.style.display = 'none'
            companyField.style.display = 'block'
            taxNumber.style.display = 'block'
            taxAdministrationInput.style.display = 'block'

            document.getElementById("id_tc").removeAttribute("required")
            document.getElementById("id_company_name").setAttribute("required", "true")
            document.getElementById("id_tax_number").setAttribute("required", "true")
            document.getElementById("id_tax_administration").setAttribute("required", "true")

        } else {
            tcField.style.display = 'none'
            companyField.style.display = 'none'
            taxNumber.style.display = 'none'
            taxAdministrationInput.style.display = 'none'
            document.getElementById("id_tc").removeAttribute("required")
            document.getElementById("id_company_name").removeAttribute("required")
            document.getElementById("id_tax_number").removeAttribute("required")
            document.getElementById("id_tax_administration").removeAttribute("required")
        }
    })


    if (billType.value != '') {
        if (billType.value == "Bireysel") {
            tcField.style.display = 'block'
            companyField.style.display = 'none'
            taxNumber.style.display = 'none'
            taxAdministrationInput.style.display = 'none'
            document.getElementById("id_tc").setAttribute("required", "true")
            document.getElementById("id_company_name").removeAttribute("required")
            document.getElementById("id_tax_number").removeAttribute("required")
            document.getElementById("id_tax_administration").removeAttribute("required")


        } else if (billType.value == "Kurumsal") {
            tcField.style.display = 'none'
            companyField.style.display = 'block'
            taxNumber.style.display = 'block'
            taxAdministrationInput.style.display = 'block'

            document.getElementById("id_tc").removeAttribute("required")
            document.getElementById("id_company_name").setAttribute("required", "true")
            document.getElementById("id_tax_number").setAttribute("required", "true")
            document.getElementById("id_tax_administration").setAttribute("required", "true")


        } else {
            tcField.style.display = 'none'
            companyField.style.display = 'none'
            taxNumber.style.display = 'none'
            taxAdministrationInput.style.display = 'none'
            document.getElementById("id_tc").removeAttribute("required")
            document.getElementById("id_company_name").removeAttribute("required")
            document.getElementById("id_tax_number").removeAttribute("required")
            document.getElementById("id_tax_administration").removeAttribute("required")
        }
    }

})