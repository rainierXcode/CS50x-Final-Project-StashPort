const addButton = document.querySelector(".collections-button")
const addNewFolder = document.querySelector(".add-new-folder")
const closeFolder = document.querySelector(".close-folder-form")
const addNewFolderButtonIinBox = document.querySelector(".add-new-folder-button")



addButton.addEventListener("click", ()=>{
    addNewFolder.style.display = "block"
})

if(closeFolder != null){
    closeFolder.addEventListener("click", (event)=>{
        event.preventDefault()
    })

}

if(addNewFolderButtonIinBox != null){
addNewFolderButtonIinBox.addEventListener("click", scrollablle)
}


const folderInput = document.getElementById("folder_name_input");
const addNewFolderButton = document.getElementById("add-new-folder-button");
const categoriesImg = document.querySelectorAll(".all_folder_image img");
let selectImage = document.getElementById("selected_image_add")

let haveInput = false;
let haveImgSelect = false;

let selectedImg = null;
categoriesImg.forEach((img) => {
  img.addEventListener("click", () => {
    if (selectedImg !== null) {
      selectedImg.classList.remove('select'); 
    }
    img.classList.add('select'); 
    selectImage.value = img.getAttribute("data_category_img")
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

function displayCurrentImg(current_img_path){
  const AllForderImg = document.querySelectorAll(".all_folder_image-EDIT img")

  AllForderImg.forEach((img)=>{
     img_path = img.getAttribute("data_category_img")

     if(img_path == current_img_path){

      AllForderImg.forEach((img)=>{
        img.classList.remove("current-category-img")
      })
      img.classList.add("current-category-img")
     }
  })

}


const editButtons = document.querySelectorAll(".folder-image-box-manipulate .material-symbols-outlined");
const categoryEditingForm = document.querySelector(".add-new-folder-home-editing")
const editingCategoryName = document.getElementById("folder_name_inputinEdit")
const AllForderImg = document.querySelectorAll(".all_folder_image-EDIT img")
let selected_image = document.getElementById("selected_image_edit")
let folderId = document.getElementById("folder_id")
const addNewFolderEditButton = document.getElementById("add-new-folder-button-EDIT")


editButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    addNewFolderEditButton.classList.remove("disabled-button")
    event.preventDefault(); 
    category_name = button.getAttribute("data-category-name")
    category_img =  button.getAttribute("data-category-img")
    folderId.value = button.getAttribute("data-folder-id")

    selected_image.value = category_img

    editingCategoryName.value = category_name
    displayCurrentImg(category_img)
    categoryEditingForm.style.display = "block"


  });
});






AllForderImg.forEach((img)=>{
    img.addEventListener("click", ()=>{
      AllForderImg.forEach((img)=>{
        img.classList.remove("current-category-img")
      })
      img.classList.add("current-category-img")
      img_path = img.getAttribute("data_category_img")
      selected_image.value = img_path
      
    })
})

let editButtonEnable = false
editingCategoryName.addEventListener("input", ()=>{
   if(editingCategoryName.value.trim() != ""){
    editButtonEnable = false
   }

   else{
    editButtonEnable = true
   }

   if(editButtonEnable){
    addNewFolderEditButton.classList.add("disabled-button")
   }
   else{
    addNewFolderEditButton.classList.remove("disabled-button")
   }
})

