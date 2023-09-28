
    




let browseFileText = document.querySelector(".browse-files");
let uploadIcon = document.querySelector(".upload-icon");
let dragDropText = document.querySelector(".dynamic-message");
let fileInput = document.querySelector(".default-file-input");
let uploadedFile = document.querySelector(".file-block");
let fileName = document.querySelector(".file-name");
let fileSize = document.querySelector(".file-size");
let progressBar = document.querySelector(".progress-bar");
let removeFileButton = document.querySelector(".remove-file-icon");
let uploadButton = document.querySelector(".upload-button");
let fileFlag = 0;

// add event listener for file input change
fileInput.addEventListener("change", e => {
  const file = fileInput.files[0];
  fileName.innerHTML = file.name;
  fileSize.innerHTML = (file.size / 1024).toFixed(1) + " KB";
  uploadedFile.style.cssText = "display: flex;";
});

// add event listener for upload button click
uploadButton.addEventListener("click", () => {
  const file = fileInput.files[0];
  if (file) {
    const formData = new FormData();
    formData.append("file", file);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload");
    xhr.upload.addEventListener("progress", e => {
      const percent = e.loaded / e.total * 100;
      progressBar.style.width = percent.toFixed(0) + "%";
    });
    xhr.addEventListener("load", () => {
      progressBar.style.width = "100%";
      uploadButton.innerHTML = `<span class="material-icons-outlined upload-button-icon"> check_circle </span> Uploaded`;
    });
    xhr.send(formData);
  }
});

// add event listener for remove file button click
removeFileButton.addEventListener("click", () => {
  uploadedFile.style.cssText = "display: none;";
  fileInput.value = '';
  progressBar.style.width = "0%";
  uploadButton.innerHTML = `Upload`;
});












