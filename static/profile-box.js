const profileClick = document.querySelector(".nav-profile-extend-box")
const profileBox= document.querySelector(".open-profile-box");
const uploadAvatarBox = document.querySelector(".right-side-upload")

if (profileClick && profileBox) {
    let isProfileBoxVisible = false;
  
    profileClick.addEventListener('click', () => {
      if (!isProfileBoxVisible) {
        profileBox.style.display = "block";
        profileClick.classList.add("box-active")
        if(uploadAvatarBox != null){
        uploadAvatarBox.classList.add("box-active")
        }
        
        isProfileBoxVisible = true;
      } else {
        profileBox.style.display = "none";
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
})}

const avatarBox = document.querySelector(".pick-avatar");
const close = document.querySelector(".avatar-close");

if (img != null){
img.addEventListener("click", ()=>{
    avatarBox.style.display = "block";
    profileBox.style.display = 'none'
});
}


if (close != null){
close.addEventListener("click", ()=>{
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

        if ( currentAvatar.value != avatarValue.value){

            avatarImg.forEach(img=>{
                img.classList.remove("current_avatar")
            })
            img.classList.add("current_avatar")
            avatarValue.value = img.getAttribute("data-avatar")
        }
        
    });
});
}



  

  const homeAvatar = document.querySelector(".home-avatar img")
 
  if (homeAvatar != null){
    homeAvatar.addEventListener("click", ()=>{
        avatarBox.style.display = "block";
    });
    }
    
    
    if (close != null){
    close.addEventListener("click", ()=>{
        avatarBox.style.display = "none"
    });
    }

