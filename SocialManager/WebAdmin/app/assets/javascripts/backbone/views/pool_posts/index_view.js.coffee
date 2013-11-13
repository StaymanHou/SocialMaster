WebAdmin.Views.PoolPosts ||= {}

class WebAdmin.Views.PoolPosts.IndexView extends Backbone.View
  template: JST["backbone/templates/pool_posts/index"]

  preventLoad: false

  events:
    'scroll': 'scroll'

  tagName: 'tbody'

  initialize: () ->
    @options.poolPosts.bind('reset', @addAll)

  addAll: () =>
    @options.poolPosts.each(@addOne)
    @options.cursor += @options.poolPosts.length
    if @options.poolPosts.length == 30
      @preventLoad = false

  addOne: (poolPost) =>
    view = new WebAdmin.Views.PoolPosts.PoolPostView({model : poolPost, sitelist: @options.sitelist, accsettingsti: @options.accsettingsti})
    @.$el.append(view.render().el)

  scroll: ->
    if not @preventLoad and @$el.children().last().offset().top - @$el.children().last().height() <= @$el.height()
      @preventLoad = true
      @options.poolPosts.fetch
        reset: true
        data: $.param
          account_id: @options.account_id
          hidden: false
          cursor: @options.cursor

  render: =>
    $(@el).html(@template(poolPosts: @options.poolPosts.toJSON() ))
    @addAll()

    return this
