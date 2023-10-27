const dashButton = document.querySelector(".dashboard-box");
const dashText = document.querySelectorAll(".dash-text");
const dashboardText = document.getElementById("dashboard-text");
const sidebar = document.querySelector(".sidebar");
const dashboardIcon = document.querySelector('.dashboard-icon');
const article = document.querySelector(".article-history");
const iconDash = document.querySelectorAll(".icon-dash");
const iconDashboard = document.querySelector(".icon-dashboard");


dashButton.addEventListener('click', () => {
    dashText.forEach((text) => {
        text.classList.toggle('hide');
    });
    dashboardText.classList.toggle('hide');
    sidebar.classList.toggle('hide');
    dashButton.classList.toggle('hide');
    dashboardIcon.classList.toggle('hide'); 
    article.classList.toggle('hide');
    iconDashboard.classList.toggle('hide');

    iconDash.forEach((icon) => {
        icon.classList.toggle('hide');
    });
    
    
});


const uploadForm = document.getElementById("upload");

