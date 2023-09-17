
const username = document.getElementById("username");
const password = document.getElementById("password");
const usernameHelper = document.querySelector(".login-username-helper");
const passwordHelper = document.querySelector(".login-password-helper");


username.addEventListener("input", ()=>{
    usernameHelper.style.display = "none";
});

password.addEventListener("input", ()=>{
    passwordHelper.style.display = "none";
});