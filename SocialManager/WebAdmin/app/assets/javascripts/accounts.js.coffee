# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

if $('body.accounts').length

	$('#rss_urls_popover').popover
		placement: 'bottom'
		title: 'Example'
		content: 'It supports multiple RSSes<br />Use comma to seperate the urls<br />e.g. "http://kpop.com/aa.rss, http://kpop.com/bb.rss"'
		html: true