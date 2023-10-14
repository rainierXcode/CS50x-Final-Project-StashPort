function editPost(){
    const form = document.querySelector(".main-post-form");
    form.style.display = "block";
}

function formClose(event){
    event.preventDefault(); 
    const form = document.querySelector(".main-post-form");
    form.style.display = "none";
}