class WebAdmin.Routers.QueuePostsRouter extends Backbone.Router
  initialize: (options) ->
    @queuePosts = new WebAdmin.Collections.QueuePostsCollection()
    @queuePosts.reset options.queuePosts

  routes:
    "new"      : "newQueuePost"
    "index"    : "index"
    ":id/edit" : "edit"
    ":id"      : "show"
    ".*"        : "index"

  newQueuePost: ->
    @view = new WebAdmin.Views.QueuePosts.NewView(collection: @queue_posts)
    $("#queue_posts").html(@view.render().el)

  index: ->
    @view = new WebAdmin.Views.QueuePosts.IndexView(queue_posts: @queue_posts)
    $("#queue_posts").html(@view.render().el)

  show: (id) ->
    queue_post = @queue_posts.get(id)

    @view = new WebAdmin.Views.QueuePosts.ShowView(model: queue_post)
    $("#queue_posts").html(@view.render().el)

  edit: (id) ->
    queue_post = @queue_posts.get(id)

    @view = new WebAdmin.Views.QueuePosts.EditView(model: queue_post)
    $("#queue_posts").html(@view.render().el)
