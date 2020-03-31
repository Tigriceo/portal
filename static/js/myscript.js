// Установка csrf_token
(function () {
    let csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        headers: {"X-CSRFToken": csrftoken}
    });
})();


// Регистрация и авторизация
function getPass() {
    let username = document.getElementById("id_username").value;
    $.ajax({
        url: "http://127.0.0.1:8000/profile/registr/",
        type: "POST",
        data: {
            username: username,
        },
        success: (response) => {
            //window.location = response
            let pass = document.getElementById("id_password");
            pass.disabled = false
        },
        error: (response) => {
            console.log("False")
        }
    })
}


// Проверка ввода номера телефона (цифры а не буквы)
(function(){
  let text = document.getElementById("id_username"),
      testText;
      text.onkeyup = function testKey(){
         let testText = text.value;
          if(testText*1 + 0  !=  text.value){
            text.value = testText.substring(0, testText.length - 1)

          }
      }
})();
