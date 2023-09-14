const signUpButton = document.querySelector(".button-signup button");
const conPass = document.getElementById("confirm-password-signup");

signUpButton.addEventListener('click', (event) => {
    event.preventDefault();
    const pass = document.getElementById("password-signup").value;

    if (pass !== conPass.value) {
        conPass.placeholder = "Password Doesn't Match";
        conPass.value = ""; 
    }
});

conPass.addEventListener('focus', () => {
    conPass.placeholder = "Confirm Password";
});
