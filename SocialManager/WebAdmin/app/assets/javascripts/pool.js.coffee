# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

if $('#rss-table').length

  account_id = $('#rss-table').data('account')
  cursor = $('#rss-table').data('cursor')
  sitelist = $('#hiddendata').data('sitelist')
  accsettingsti = $('#hiddendata').data('accsettingsti')

  @poolPosts = new WebAdmin.Collections.PoolPostsCollection()

  @view = new WebAdmin.Views.PoolPosts.IndexView
    poolPosts: @poolPosts
    account_id: account_id
    cursor: cursor
    sitelist: sitelist
    accsettingsti: accsettingsti

  @poolPosts.fetch
    reset: true
    data: $.param({ account_id: account_id, hidden: false, cursor: cursor})

  $('#rss-table').append(@view.el)

  $('.onpage-alert').on('click', ->
    $('.onpage-alert').fadeOut()
    )
