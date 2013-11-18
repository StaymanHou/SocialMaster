# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

if $('body.acc_settings').length

	$('#other_setting_popover').popover
		placement: 'bottom'
		title: 'Example'
		content: '<strong>For facebook:</strong><br />{"page_name": "kpopstarzfacebookpage", "page_path":"/kpopstarz", "page_id":"122361684544935"}<br /><strong>For google+:</strong><br />{"page_path": "/b/110422726213868653185/"}<br /><strong>For tumblr:</strong><br />{"blog_name": "kpopstarztumblrblog","link_anchor_text":"Continue Reading"}<br /><strong>For pinterest</strong>:<br />{"board_name": "KpopStarzBoard"}'
		html: true