function mascara_cpf(){
    var cpf = document.getElementById('id_cep')
    if (cpf.value.length == 3 || cpf.value.length == 7) {
        cpf.value += "."
    } else if (cpf.value.length == 11) {
        cpf.value += "."
    }
}

// function mascara_cep() {
//     var cep = document.getElementById('id_cep')
//     if (cep.value.length == 5) {
//         cep.value += "-"
//     }
// }