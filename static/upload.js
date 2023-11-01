const dashButton = document.querySelector(".dashboard-box");
const dashText = document.querySelectorAll(".dash-text");
const dashboardText = document.getElementById("dashboard-text");
const bodyContainer = document.querySelector(".body-container");
const sidebar = document.querySelector(".sidebar");
const dashboardIcon = document.querySelector('.dashboard-icon');
const header = document.querySelector(".header");
const article = document.querySelector(".article-upload");
const iconDash = document.querySelectorAll(".icon-dash");
const iconDashboard = document.querySelector(".icon-dashboard");







const uploadForm = document.getElementById("upload");


const select = document.getElementById("folders");
const createNewOption = document.getElementById("createnew");
const folderForm = document.querySelector(".add-new-folder");
const folderFormClose = document.getElementById("close-folder-form");
let isopenFolderForm = null;

select.addEventListener("change", () => {
    if (select.value === "createnew") {
        folderForm.style.display = "block";
        isopenFolderForm = true;
        folderFormClose.addEventListener("click", () => {
            folderForm.style.display = "none";
            select.value = "Folders";
        });

    }


})
const folderInput = document.getElementById("folder_name_input");
const addNewFolderButton = document.getElementById("add-new-folder-button");
const categoriesImg = document.querySelectorAll(".all_folder_image img");

let haveInput = false;
let haveImgSelect = false;

let selectedImg = null;
categoriesImg.forEach((img) => {
  img.addEventListener("click", () => {
    if (selectedImg !== null) {
      selectedImg.classList.remove('select'); 
    }
    img.classList.add('select'); 
    document.getElementById('selected_image').value = img.src;
    selectedImg = img;
    haveImgSelect = true; 
    checkEnableButton(); 
  });
});

if (folderInput != null) {
  folderInput.addEventListener("input", () => {
    if (folderInput.value.trim() !== "") {
      haveInput = true; 
    } else {
      haveInput = false; 
    }
    checkEnableButton(); 
  });

  function checkEnableButton() {
    if (haveInput && haveImgSelect) {
      addNewFolderButton.classList.remove("disabled-button");
    } else {
      addNewFolderButton.classList.add("disabled-button");
    }
  }
}


if(folderInput != null){
folderFormClose.addEventListener("click", () => {
    addNewFolderButton.classList.add("disabled-button");
    folderInput.value = "";
});
}

const allErrorCLose = document.querySelector(".all_error_post-header div:nth-child(2) button");
const allErrorBox = document.querySelector(".all_error_post");

if (allErrorBox != null) {
    const allErrorCLose = document.querySelector(".all_error_post-header div:nth-child(2) button");
    allErrorCLose.addEventListener("click", () => {
        allErrorBox.style.display = "none";
    });

}

