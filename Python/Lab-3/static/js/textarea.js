textarea = document.querySelector("#textarea");

textarea.addEventListener('input', autoResize, false);

function autoResize() {
   this.style.height = 'auto';
   this.style.height = this.scrollHeight + 'px';
}