const fname = document.getElementById("fname");
const fnameHelper = document.querySelector(".signup-fname-helper");

const lname = document.getElementById("lname");
const lnameHelper = document.querySelector(".signup-lname-helper");

const username = document.getElementById("username-signup");
const usernameHelper = document.querySelector(".signup-username-helper");

const password = document.getElementById("password-signup");
const passwordHelper = document.querySelector(".signup-password-helper");

const confirm_password = document.getElementById("confirm-password-signup");
const confirm_passwordHelper = document.querySelector(".signup-confirm_password-helper");

fname.addEventListener("input", ()=>{
    fnameHelper.style.display = "none";
});

lname.addEventListener("input", ()=>{
    lnameHelper.style.display = "none";
});

username.addEventListener("input", ()=>{
    usernameHelper.style.display = "none";
});

password.addEventListener("input", ()=>{
    passwordHelper.style.display = "none";
});

confirm_password.addEventListener("input", ()=>{
    confirm_passwordHelper.style.display = "none";
});

