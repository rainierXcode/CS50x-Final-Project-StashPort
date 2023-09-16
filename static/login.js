// let loginForm = document.getElementById("login-button");
let username = document.getElementById("username");
let password = document.getElementById("password");
let usernameHelper = document.querySelector(".login-username-helper");
let passwordHelper = document.querySelector(".login-password-helper");

// loginForm.addEventListener('click', (event) => {
//     const trimmedUsername = username.value.trim();
//     const trimmedPassword = password.value.trim();

//     // Username validation
//     if (trimmedUsername === "") {
//         event.preventDefault();
//         usernameHelper.style.display = "block";
//         usernameHelper.textContent = "Please enter a username";
//     } else if (trimmedUsername.length < 6 || trimmedUsername.length > 120) {
//         event.preventDefault();
//         usernameHelper.style.display = "block";
//         usernameHelper.textContent = "Username must be between 6 and 120 characters";
//     }

    
//     else{
//         usernameHelper.style.display = "none";
//     }

//     // Password validation
//     if (trimmedPassword === "") {
//         event.preventDefault();
//         passwordHelper.style.display = "block";
//         passwordHelper.textContent = "Please enter a password";
//     } else if (trimmedPassword.length < 6) {
//         event.preventDefault();
//         passwordHelper.style.display = "block";
//         passwordHelper.textContent = "The password must have at least 6 characters";
//     }

//     else{
//         passwordHelper.style.display = "none";
//     }
// });

username.addEventListener("input", ()=>{
    usernameHelper.style.display = "none";
});

password.addEventListener("input", ()=>{
    passwordHelper.style.display = "none";
});