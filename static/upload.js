const dashButton = document.querySelector(".dashboard-box");
const dashText = document.querySelectorAll(".dash-text");
const dashboardText = document.getElementById("dashboard-text");
const bodyContainer = document.querySelector(".body-container");
const sidebar = document.querySelector(".sidebar");
const dashboardIcon = document.querySelector('.dashboard-icon');
const header  = document.querySelector(".header");
const article = document.querySelector(".article-upload");
const iconDash = document.querySelectorAll(".icon-dash");
const iconDashboard = document.querySelector(".icon-dashboard");




dashButton.addEventListener('click', () => {
    dashText.forEach((text) => {
        text.classList.toggle('hide');
    });
    dashboardText.classList.toggle('hide');
    bodyContainer.classList.toggle('hide');
    sidebar.classList.toggle('hide');
    dashButton.classList.toggle('hide');
    dashboardIcon.classList.toggle('hide');
    header.classList.toggle('hide');
    article.classList.toggle('hide');
    iconDashboard.classList.toggle('hide');

    iconDash.forEach((icon) => {
        icon.classList.toggle('hide');
    });
    
    
});


const uploadForm = document.getElementById("upload");


const select = document.getElementById("folders");
const createNewOption = document.getElementById("createnew");
const folderForm = document.querySelector(".add-new-folder");
const folderFormClose = document.getElementById("close-folder-form");
let isopenFolderForm = null;

select.addEventListener("change", () =>{
      if(select.value === "createnew"){
        folderForm.style.display = "block";
        isopenFolderForm = true;
        folderFormClose.addEventListener("click", () =>{
            folderForm.style.display = "none";
            select.value = "Folders";
        });
        
    }

})


const folderInput = document.getElementById("folder_name_input");
const addNewFolderButton = document.getElementById("add-new-folder-button");


folderInput.addEventListener("input", () =>{
    addNewFolderButton.classList.remove("disabled-button");
});

folderFormClose.addEventListener("click", () =>{
    addNewFolderButton.classList.add("disabled-button");
    folderInput.value = "";
});