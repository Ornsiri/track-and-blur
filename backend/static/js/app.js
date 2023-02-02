'use strict'



// // Show/Hide password 
// function showAndHidePassword() {
//     var x = document.body.innerHTML.getElementById("password-signin");
//     var show_eye = document.body.innerHTML.getElementById("show_eye");
//     var hide_eye = document.body.innerHTML.getElementById("hide_eye");
//     hide_eye.classList.remove("d-none");
//     if (x.type === "password") {
//         x.type = "text";
//         show_eye.style.display = "none";
//         hide_eye.style.display = "block";
//     } else {
//         x.type = "password";
//         show_eye.style.display = "block";
//         hide_eye.style.display = "none";
//     }
// }

// // Form validation
// (() => {

//     // Fetch all the forms we want to apply custom Bootstrap validation styles to
//     const forms = document.body.innerHTML.querySelectorAll('.needs-validation')

//     // Loop over them and prevent submission
//     Array.from(forms).forEach(form => {
//         form.addEventListener('submit', event => {
//             if (!form.checkValidity()) {
//                 event.preventDefault()
//                 event.stopPropagation()
//             }

//             form.classList.add('was-validated')
//         }, false)
//     })
// })()