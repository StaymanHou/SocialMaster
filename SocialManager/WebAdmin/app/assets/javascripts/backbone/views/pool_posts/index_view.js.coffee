WebAdmin.Views.PoolPosts ||= {}

class WebAdmin.Views.PoolPosts.IndexView extends Backbone.View
  template: JST["backbone/templates/pool_posts/index"]

  preventLoad: false

  events:
    'scroll': 'scroll'

  tagName: 'tbody'

  initialize: () ->
    @options.poolPosts.bind('reset', @addAll)
    @options.latest = null
    @options.fn = false

  addAll: () =>
    if @options.fn
      @options.poolPosts.each(@insertOne)
      if @options.poolPosts.length > 0
        @options.latest = @options.poolPosts.last().id
        new_pop = $('#new-pop')
        counter = new_pop.data('counter')
        counter += @options.poolPosts.length
        $('#new-pop-counter').html(counter)
        new_pop.data('counter', counter)
        new_pop.css('display','block')

    else
      @options.poolPosts.each(@addOne)
      if @options.latest is null
        @options.latest = @options.poolPosts.first().id
        window.setInterval(_.bind(@fetch_new, @), 60000);
      if @options.poolPosts.length > 0
        @options.cursor = @options.poolPosts.last().id
      if @options.poolPosts.length == 30
        @preventLoad = false

  addOne: (poolPost) =>
    view = new WebAdmin.Views.PoolPosts.PoolPostView({model : poolPost, sitelist: @options.sitelist, accsettingsti: @options.accsettingsti})
    @.$el.append(view.render().el)

  insertOne: (poolPost) =>
    view = new WebAdmin.Views.PoolPosts.PoolPostView({model : poolPost, sitelist: @options.sitelist, accsettingsti: @options.accsettingsti})
    @.$el.prepend(view.render().$el.addClass('new-feed hide'))

  scroll: ->
    if not @preventLoad and @$el.children().last().offset().top - @$el.children().last().height() <= @$el.height()
      @preventLoad = true
      @options.fn = false
      @options.poolPosts.fetch
        reset: true
        data: $.param
          account_id: @options.account_id
          hidden: false
          cursor: @options.cursor

  fetch_new: ->
    fetch_new_success_callback = @fetch_new_success_callback
    @options.fn = true
    @options.poolPosts.fetch
      reset: true
      data: $.param
        account_id: @options.account_id
        hidden: false
        cursor: -1
        latest: @options.latest

  render: =>
    $(@el).html(@template(poolPosts: @options.poolPosts.toJSON() ))
    @addAll()

    return this
