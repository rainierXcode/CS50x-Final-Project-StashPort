const signUpForm = document.getElementById("sign-up-button");
const conPass = document.getElementById("confirm-password-signup");

signUpForm.addEventListener('click', (event) => {
    const pass = document.getElementById("password-signup").value;

    if (pass !== conPass.value) {
        event.preventDefault(); 
        conPass.placeholder = "Password Doesn't Match";
        conPass.value = ""; 
    }
    alert("h");
});

conPass.addEventListener('focus', () => {
    conPass.placeholder = "Confirm Password";
});


