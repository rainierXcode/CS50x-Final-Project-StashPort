function editPost(){
    const form = document.querySelector(".main-post-form");
    form.style.display = "block";
}

const formClose = document.querySelector(".main-post-form-close-button")
formClose.addEventListener("click", (event)=>{
    event.preventDefault(); 
    const form = document.querySelector(".main-post-form");
    form.style.display = "none";
}
)