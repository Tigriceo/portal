// $(function(){
//     let form = $('#delete_form');
//     console.log("ok1");
//     form.on("submit", function(e){
//         e.preventDefault();
//         console.log(form);
//
//         var delete_btn = $('delete');
//         var data_new = delete_btn.data('newdata');
//         var csrf_token = $('#delete_form [name="csrfmiddlewaretoken"]').val();
//         var url = form.attr("action");
//         console.log(data_new, csrf_token, url)
//
//             var data = {};
//             data.data_new = data_new;
//             data.csrfmiddlewaretoken = csrf_token;
//
//
//             $.ajax({
//                 url: url,
//                 type: 'POST',
//                 // dataType: 'json',
//                 data: data,
//                 cache: true,
//                 success: function(){
//                     alert('ok')
//                     },
//                 error: function() {
//                     console.log('error')
//                 }
//             })
//     });
// });