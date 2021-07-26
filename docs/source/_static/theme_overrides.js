$(document).ready(function() {
	var path = '';
	
	if($('.icon.icon-home').attr('href') == '../index.html') path = '../';
	else if($('.icon.icon-home').attr('href') == '../../index.html') path = '../../';
		
	$('.icon.icon-home').html('<img src="' + path + '_static/logo.png" class="logo" alt="Logo">');
});