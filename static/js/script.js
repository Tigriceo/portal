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
	$('.addpage-img input[type="file"]').change(function(e){
        let value = e.target.files[0].name;
        $(this).closest('.addpage-img').find('div').text(value);
    });

});