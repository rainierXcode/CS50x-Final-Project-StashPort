const profileClick = document.querySelector(".nav-profile-extend-box")
const profileBox= document.querySelector(".open-profile-box");
const uploadAvatarBox = document.querySelector(".right-side-upload")
const searchButton = document.querySelector(".searchInput label")
const search = document.querySelector(".searchInput")

function unclickableThem(){

    const middleNav = document.querySelector(".middle-nav")
    const sidebar = document.querySelector(".sidebar")
    const searchHome = document.querySelector(".header-top label")
    const upload = document.querySelector(".header-down-right a")
    const thumbnailBox = document.querySelector(".thumbnail-box")
    const newUploadBox = document.querySelector(".new-upload-post-box a")
    if (window.innerWidth < 768){
        if(search != null) { search.classList.add('unclickable')}
        if(middleNav !=null) { middleNav.classList.add('unclickable')}
        if(profileClick !=null) {profileClick.classList.add('unclickable')}
        if(sidebar !=null) {sidebar.classList.add('unclickable')}
        if(searchHome !=null) {searchHome.classList.add('unclickable')}
        if(upload !=null) {upload.classList.add('unclickable')}
        if(thumbnailBox !=null) {thumbnailBox.classList.add('unclickable')}
        if(newUploadBox !=null) {newUploadBox.classList.add('unclickable')}

    }
}

function clickableThem(){

    const middleNav = document.querySelector(".middle-nav")
    const sidebar = document.querySelector(".sidebar")
    const searchHome = document.querySelector(".header-top label")
    const upload = document.querySelector(".header-down-right a")
    const thumbnailBox = document.querySelector(".thumbnail-box")
    const newUploadBox = document.querySelector(".new-upload-post-box a")
    if (window.innerWidth < 768){
        if(search != null) { search.classList.remove('unclickable')}
        if(middleNav !=null) { middleNav.classList.remove('unclickable')}
        if(profileClick !=null) {profileClick.classList.remove('unclickable')}
        if(sidebar !=null) {sidebar.classList.add('unclickable')}
        if(searchHome !=null) {searchHome.classList.add('unclickable')}
        if(upload !=null) {upload.classList.add('unclickable')}
        if(thumbnailBox !=null) {thumbnailBox.classList.add('unclickable')}
        if(newUploadBox !=null) {newUploadBox.classList.add('unclickable')}
    }
}


  

function blurMe(){
    const article = document.querySelector(".article")
    const header = document.querySelector(".header")
    const sidebar = document.querySelector(".sidebar")
    const nav = document.querySelector(".nav")

    if(window.innerWidth < 768){

        if(article != null){ article.classList.add("blurme") }

        if(header != null){ header.classList.add("blurme") }

        if(sidebar != null){ sidebar.classList.add("blurme") }

        if(nav != null){ nav.classList.add("blurme") }
       
        
    }
}

function unBlurMe(){
    if(window.innerWidth < 768){
    const article = document.querySelector(".article")
    const header = document.querySelector(".header")
    const sidebar = document.querySelector(".sidebar")
    const nav = document.querySelector(".nav")


    if(article != null){ article.classList.remove("blurme") }

    if(header != null){ header.classList.remove("blurme") }

    if(sidebar != null){ sidebar.classList.remove("blurme") }

    if(nav != null){ nav.classList.remove("blurme") }
    }
}

if (profileClick && profileBox) {
    let isProfileBoxVisible = false;
  
    profileClick.addEventListener('click', () => {
      
      if (!isProfileBoxVisible) {
        profileBox.style.display = "block";
        
        
        if(window.innerWidth < 768 && search != null){
            search.classList.add("unclickable")
        }

        profileClick.classList.add("box-active")
        if(uploadAvatarBox != null){
        uploadAvatarBox.classList.add("box-active")
        }
        
        isProfileBoxVisible = true;
      } else {
        profileBox.style.display = "none";

        if(window.innerWidth < 768 && search != null){
            search.classList.remove("unclickable")
        }

        profileClick.classList.remove("box-active")
        if(uploadAvatarBox != null){
        uploadAvatarBox.classList.remove("box-active")
        }
        isProfileBoxVisible = false;
      }
    });
  }


const img = document.querySelector(".profile-corner");
const editText = document.querySelector(".profile-corner div");

if (img != null){
img.addEventListener("mouseover", ()=>{
 
    editText.style.display = "block";
});

img.addEventListener("mouseout", ()=>{
    editText.style.display = "none";
    profileClick.classList.remove("box-active")
    
})}

const avatarBox = document.querySelector(".pick-avatar");
const close = document.querySelector(".avatar-close");

if (img != null){
img.addEventListener("click", ()=>{

    avatarBox.style.display = "block";
    blurMe()
    unclickableThem()
    profileBox.style.display = 'none'
});
}


if (close != null){
close.addEventListener("click", ()=>{
    unBlurMe()
    clickableThem()
    avatarBox.style.display = "none"
});
}

const avatarImg = document.querySelectorAll(".avatargrid img");
let avatarValue = document.getElementById("selected_avatar");
let currentAvatar = document.getElementById("current_avatar");


if (avatarImg != null){
avatarImg.forEach(img => {
    img.addEventListener('click', () => {
        avatarValue.value = img.getAttribute("data-avatar")
            avatarImg.forEach(img =>{
                img.classList.remove("current_avatar")
            })
            img.classList.add("current_avatar")
            

           
    });
});
}



  

  const homeAvatar = document.querySelector(".home-avatar img")
 
  if (homeAvatar != null){
    homeAvatar.addEventListener("click", ()=>{
        blurMe()
        unclickableThem()
        avatarBox.style.display = "block";
    });
    }
    
    
    if (close != null){
    close.addEventListener("click", ()=>{
        avatarBox.style.display = "none"
        unBlurMe()
        clickableThem()
    });
    }




if (window.innerWidth < 768 ){


const searchInput = document.querySelector(".searchInput input")
const middleNav = document.querySelector(".middle-nav")
const navProfile = document.querySelector(".nav-profile")


  if(searchButton != null){
    let isButtonOpen = false
    searchButton.addEventListener("click", ()=>{
        if(!isButtonOpen){
            searchInput.style.display = "block"
            middleNav.style.display = "none"
            navProfile.style.display = "none"
            isButtonOpen = true
        }

        else{
            searchInput.style.display = "none"
            middleNav.style.display = "flex"
            navProfile.style.display = "flex"
            isButtonOpen = false
        }
    })
}

}

