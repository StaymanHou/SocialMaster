# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

waterfallOffset = $('.waterfall').offset().top
headers = $('.waterfall-header').clone()
fixedHeaders = $('#fixedHeader')
fixedHeaders.hide()
headers.each ->
	wrap = $('<div>', {class: 'waterfall-column'})
	wrap.append(@)
	fixedHeaders.append(wrap)

$(window).bind("scroll", ->
    offset = $(@).scrollTop()+40

    console.log(offset)
    console.log(waterfallOffset)

    if offset >= waterfallOffset and fixedHeaders.is(":hidden")
        fixedHeaders.show()
    
    else if offset < waterfallOffset
        fixedHeaders.hide()
)