  document.getElementById('activateBtn').addEventListener('click', function(event) {
    var fio = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var repeat_password = document.getElementById('confirmPassword').value;
    var identification_key = document.getElementById('key').value; // Получаем введенный ключ

    if (!fio || !email || !password || !repeat_password || !identification_key) {
      alert('Пожалуйста, заполните все поля в первом контейнере перед отправкой.');
      event.preventDefault();
    }
          // Дополнительная проверка ключа
    if (identification_key !== 'dsff-ndfh-nghf-gfdg') {
        alert('Неверный ключ идентификации.');
        event.preventDefault();
    }
  });
    document.addEventListener("DOMContentLoaded", function() {
      var container2 = document.querySelector('.container2 .wrapper');
      var rowButton = document.querySelector('.row_button');
      var pass = document.querySelector('.pass');

      container2.insertBefore(rowButton, pass);
    });



  function displayFileName(input) {
    var fileName = input.files[0].name;
    var fileNameDisplay = document.getElementById('fileNameDisplay');
    var filename = (fileName.length > 32) ? '...' + fileName.substring(fileName.length - 32) : fileName;
    fileNameDisplay.innerText = filename;
  }