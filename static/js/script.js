jQuery(document).ready(function () {
	$(".cat-menu-link").click(function () {
		$(this).toggleClass('menu-swipe');
		$(".menu-bg").toggleClass('menu-open');
		$(".menu-close").toggleClass('menu-load');
	});
	$(".menu-close").click(function () {
		$(".cat-menu-link").toggleClass('menu-swipe');
		$(".menu-bg").toggleClass('menu-open');
		$(".menu-close").toggleClass('menu-load');
	});
	$('.city-select select').chosen({
		width: "100%",
		no_results_text: "Ваш город скоро появится: "
	});
	$('.addform-select select').chosen({
		width: "50%",
		disable_search: true,
	});

	$('.sort-block select').chosen({
		width: "180px",
		disable_search: true,
	});


	$('.city-select select').change(function (evt) {
		name = $(this).val();
		$("#city-selected").text(name);
	});

	$(function () {
		$('.chat-slider').slick({
			vertical: true,
			verticalSwiping: true,
			slidesToShow: 3,
			autoplay: false,
		});
	});

	$(".addpage-img").click(function () {
        $(this).find('input[type="file"]')[0].click();
	});

	$(".profile-photo").click(function () {
        $(this).find('input[type="file"]')[0].click();
	});


	$('.addpage-img input[type="file"]').change(function(e){
        let value = e.target.files[0].name;
        $(this).closest('.addpage-img').find('div').text(value);
	});

	$('.datepicker-here').datepicker({
		// Можно выбрать тольо даты, идущие за сегодняшним днем, включая сегодня
		minDate: new Date()
	})

	$(".addform-todaybut").click(function () {
		var d = new Date();
		d.setDate(d.getDate() + 1);
		$(".datepicker-here").val(((d.getDate() > 9) ? d.getDate() : ('0' + d.getDate())) + '.' + ((d.getMonth() > 8) ? (d.getMonth() + 1) : ('0' + (d.getMonth() + 1))) + '.' + d.getFullYear());
	});

	$('.modal-form-login #submit').prop('disabled', true);

	$('.modal-form-login #check1').change(function(){
if ($(this).prop('checked')){
	$('.modal-form-login #submit').prop('disabled', false);
}else{
	$('.modal-form-login #submit').prop('disabled', true);
}
	})
	
});
 
