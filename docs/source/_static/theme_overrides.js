$(document).ready(function() {
	var path = '';
	
	if($('.wy-side-nav-search .icon.icon-home').attr('href') == '../index.html') path = '../';
	else if($('.wy-side-nav-search .icon.icon-home').attr('href') == '../../index.html') path = '../../';
		
	$('.wy-side-nav-search .icon.icon-home').html('<img src="' + path + '_static/logo_alpha.png" class="logo" alt="Logo" style="width:110px;">');
});