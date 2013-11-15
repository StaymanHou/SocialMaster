# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

if $('div.waterfall').length

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

      if offset >= waterfallOffset and fixedHeaders.is(":hidden")
          fixedHeaders.show()
      
      else if offset < waterfallOffset
          fixedHeaders.hide()
  )

  smodulelist = $('#hiddendata').data('smodulelist')
  accsettingsti = $('#hiddendata').data('accsettingsti')
  cursor = 0

  $.each( smodulelist, ->
    acc_setting = accsettingsti[@name]
    queuePosts = new WebAdmin.Collections.QueuePostsCollection()

    view = new WebAdmin.Views.QueuePosts.IndexView
      queuePosts: queuePosts
      smodule: @
      acc_setting: acc_setting
      cursor: 0

    queuePosts.fetch
      reset: true
      data: $.param
        acc_setting_id: acc_setting.id
        cursor: 0

    $('#accordionacc .waterfall-header.'+@name+'header').after(view.el)

    $('.onpage-alert').on('click', ->
      $('.onpage-alert').fadeOut()
    )

  )

