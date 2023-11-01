
const allErrorCLose = document.querySelector(".all_error_post-header div:nth-child(2) button");
const allErrorBox = document.querySelector(".all_error_post");

if (allErrorBox != null) {
    const allErrorCLose = document.querySelector(".all_error_post-header div:nth-child(2) button");
    allErrorCLose.addEventListener("click", () => {
        allErrorBox.style.display = "none";
    });

}

const originalBox = document.querySelector(".main-post")
const formBox  = document.querySelector(".post-textbox-upload")
const originalBoxEditButton = document.querySelector(".main-post-edit-button")
const formBoxCloseButton = document.querySelector(".main-post-form-close-button")

originalBoxEditButton.addEventListener("click", ()=>{
     originalBox.style.display = "none"
     formBox.style.display = "block"
})


formBoxCloseButton.addEventListener("click", ()=>{
   formBox.style.display = "none"
   originalBox.style.display = "block"
})