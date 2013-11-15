WebAdmin.Views.QueuePosts ||= {}

class WebAdmin.Views.QueuePosts.IndexView extends Backbone.View
  template: JST["backbone/templates/queue_posts/index"]

  preventLoad: true

  className: 'waterfall-body'

  initialize: () ->
    @options.queuePosts.bind('reset', @addAll)
    _.bindAll(this, 'scroll')
    $(window).scroll(this.scroll)

  addAll: () =>
    @options.queuePosts.each(@addOne)
    if @options.queuePosts.length > 0
      @options.cursor += @options.queuePosts.length
    if @options.queuePosts.length == 30
      @preventLoad = false

  addOne: (queuePost) =>
    view = new WebAdmin.Views.QueuePosts.QueuePostWaterfallView
      model: queuePost
      parent: @
      smodule: @options.smodule.name
    $(@el).append(view.render().el)

  scroll: () ->
    if not @preventLoad and @$el.children().last().offset().top <= $(window).scrollTop() + $(window).height()
      @preventLoad = true
      @options.queuePosts.fetch
        reset: true
        data: $.param
          acc_setting_id: @options.acc_setting.id
          cursor: @options.cursor

  pop_queue_number: (smodule) ->
    count = $('.waterfall-header.'+smodule+'header').data('count')
    count -= 1
    $('.waterfall-header.'+smodule+'header').data('count', count)
    $('.waterfall-header.'+smodule+'header span').html(count)

  render: =>
    $(@el).html(@template(queuePosts: @options.queuePosts.toJSON() ))
    @addAll()

    return this
