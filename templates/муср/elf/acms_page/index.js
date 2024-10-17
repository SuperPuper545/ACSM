
let menuicn = document.querySelector(".menuicn"); 
let nav = document.querySelector(".navcontainer"); 
  
menuicn.addEventListener("click", () => { 
    nav.classList.toggle("navclose"); 
})

//
// Переключение темы
//
document.getElementById('themeToggle').addEventListener('click', function() {
  const currentTheme = document.body.className;
  if (currentTheme === 'light-theme') {
      document.body.className = 'dark-theme';
  } else {
      document.body.className = 'light-theme';
  }
});

//
// Модальное окно
//
const exampleModal = document.getElementById('view')
if (exampleModal) {
  exampleModal.addEventListener('show.bs.modal', event => {
    // Button that triggered the modal
    const button = event.relatedTarget
    // Extract info from data-bs-* attributes
    const recipient = button.getAttribute('data-bs-whatever')
    // If necessary, you could initiate an Ajax request here
    // and then do the updating in a callback.

    // Update the modal's content.
    const modalTitle = exampleModal.querySelector('.modal-title')
    const modalBodyInput = exampleModal.querySelector('.modal-body input')

    modalTitle.textContent = `New message to ${recipient}`
    modalBodyInput.value = recipient
  })
}

