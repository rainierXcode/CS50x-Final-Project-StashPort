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


