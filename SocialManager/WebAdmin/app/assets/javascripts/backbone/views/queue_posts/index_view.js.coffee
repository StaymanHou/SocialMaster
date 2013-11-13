WebAdmin.Views.QueuePosts ||= {}

class WebAdmin.Views.QueuePosts.IndexView extends Backbone.View
  template: JST["backbone/templates/queue_posts/index"]

  initialize: () ->
    @options.queuePosts.bind('reset', @addAll)

  addAll: () =>
    @options.queuePosts.each(@addOne)

  addOne: (queuePost) =>
    view = new WebAdmin.Views.QueuePosts.QueuePostView({model : queuePost})
    @$("tbody").append(view.render().el)

  render: =>
    $(@el).html(@template(queuePosts: @options.queuePosts.toJSON() ))
    @addAll()

    return this
