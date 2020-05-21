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
    // Изменяем текст кнопки послее ее нажатия
    let elem = document.querySelector('#btn');
    elem.setAttribute('value', 'Пароль отправлен на указанный номер');
    elem.style.background = "#eb3a9a";
    // elem.disabled = true;
}

// Проверяем ввод номера телефона
document.querySelector("input[name='username']").oninput = e => e.target.value = e.target.value.replace(/\D/g, '');

// отображение миниатюры при добавлении фотографии
function readURL(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
            $('#photo').attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}