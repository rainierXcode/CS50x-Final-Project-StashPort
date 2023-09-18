
const username = document.getElementById("username");
const password = document.getElementById("password");
const usernameHelper = document.querySelector(".login-username-helper");
const passwordHelper = document.querySelector(".login-password-helper");

if (usernameHelper){
username.addEventListener("input", ()=>{
    usernameHelper.style.display = "none";
});
}

if (passwordHelper){
password.addEventListener("input", ()=>{
    passwordHelper.style.display = "none";
});
}