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

	$(".chat-block .chat-hide").click(function () {
		$(this).toggleClass('chat-showed');
		$(this).closest('.chat-block').find('.chat-header').toggleClass('chat-showed-h');
		$(this).closest('.chat-block').find('.chat-precontent').slideToggle(300);
		$(this).closest('.chat-block').find(".chat-form").slideToggle(300);
	});

	jQuery('.menu-ul > li > a').on('click', function (e) {
		e.preventDefault(); // этот код предотвращает стандартное поведение браузера по клику
		// остальной код
	});


});