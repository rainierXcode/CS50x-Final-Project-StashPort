const dashButton = document.querySelector(".dashboard-box");
const dashText = document.querySelectorAll(".dash-text");
const dashboardText = document.getElementById("dashboard-text");
const bodyContainer = document.querySelector(".body-container");
const sidebar = document.querySelector(".sidebar");
const dashboardIcon = document.querySelector('.dashboard-icon');
const header  = document.querySelector(".header");
const article = document.querySelector(".article");
const iconDash = document.querySelectorAll(".icon-dash");
const iconDashboard = document.querySelector(".icon-dashboard");

const uploadForm = document.getElementById("upload");

const searchIcon = document.querySelector(".header-top label");
const searchInput = document.querySelector(".header-top input");


let dashboardisOpen = true
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


    if(dashboardisOpen){
    searchIcon.classList.add("unclickable")
    dashboardisOpen = false
    }
    else{
        searchIcon.classList.remove("unclickable")
        dashboardisOpen = true
    }

    iconDash.forEach((icon) => {
        icon.classList.toggle('hide');
    });
    
    
});





let isNotOpen = true

searchIcon.addEventListener("click", ()=>{
    if (isNotOpen){
        searchInput.style.display = "block"
        searchInput.classList.toggle("expand")
        sidebar.style.display = "none"
        isNotOpen = false;
    
    }
    else{
        searchInput.style.display = "none"
        sidebar.style.display = "flex"

        searchInput.classList.remove("expand")
        isNotOpen = true

       
    }
})



