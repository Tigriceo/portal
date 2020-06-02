// Установка csrf_token
(function () {
    let csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        headers: {"X-CSRFToken": csrftoken}
    });
})();



function startTimer(duration) {
    var timer = duration, seconds;
        var tickersms =setInterval(function () {
        if(seconds==0){
            clearInterval(tickersms);
            window.localStorage.setItem("seconds",0);//Если у тебя будет где нибудь на серваке тикать, это можно убрать
            $('#btn').prop('disabled', false);
            $('#btn').val('Получить пароль еще раз');
        }else{
            seconds = parseInt(timer % 60, 10);
            seconds = seconds < 10 ? "0" + seconds : seconds;
            $('#btn').val('Пароль выслан. Повторно через: '+seconds+'сек.');
            $('#btn').prop('disabled', true);
            if (--timer < 0) {
                timer = duration;
            }
          console.log(parseInt(seconds));
          window.localStorage.setItem("seconds",seconds);//Сюда тоже можно свою переменную
        }
    }, 1000);
}

window.onload = function () {
    sec  = parseInt(window.localStorage.getItem("seconds"));//Если у тебя будет где нибудь на серваке тикать, можно сюда переменную секунд поставить
    if (sec >= 0){
        startTimer(sec);
    }
};

$( "#regform" ).submit(function() {
    let phonecode = $("#id_username").intlTelInput("getSelectedCountryData").dialCode;
    let username = '+'+phonecode+$("#id_username").val();
    $("#id_username").val(username);
    console.log($("#id_username").val());
    return true;
  });

// Регистрация и авторизация
function getPass() {

    startTimer(30);

    let phonecode = $("#id_username").intlTelInput("getSelectedCountryData").dialCode;
    let username = '+'+phonecode+$("#id_username").val();
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
    //let elem = document.querySelector('#btn');
    //elem.setAttribute('value', 'Пароль отправлен на указанный номер');
    //elem.style.background = "#eb3a9a";
    // elem.disabled = true;
}



// Проверяем ввод номера телефона
//document.querySelector("input[name='username']").oninput = e => e.target.value = e.target.value.replace(/\D/g, '');

// отображение миниатюры при добавлении фотографии
function readURL(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
            $('#photo').attr('src', e.target.result);
            $('.profile-photo').css('background-image', 'url(' + e.target.result + ')');
        };

        reader.readAsDataURL(input.files[0]);
    }
}

// подгружаем контент при скроле
    let infinite = new Waypoint.Infinite({
      element: $('.infinite-container')[0],
      onBeforePageLoad: function () {
        $('.loading').show();
      },
      onAfterPageLoad: function ($items) {
        $('.loading').hide();
      }
    });