class WebAdmin.Routers.PoolPostsRouter extends Backbone.Router
  initialize: (options) ->
    @poolPosts = new WebAdmin.Collections.PoolPostsCollection()
    @poolPosts.reset options.poolPosts

  routes:
    "new"      : "newPoolPost"
    "index"    : "index"
    ":id/edit" : "edit"
    ":id"      : "show"
    ".*"        : "index"

  newPoolPost: ->
    @view = new WebAdmin.Views.PoolPosts.NewView(collection: @pool_posts)
    $("#pool_posts").html(@view.render().el)

  index: ->
    @view = new WebAdmin.Views.PoolPosts.IndexView(pool_posts: @pool_posts)
    $("#pool_posts").html(@view.render().el)

  show: (id) ->
    pool_post = @pool_posts.get(id)

    @view = new WebAdmin.Views.PoolPosts.ShowView(model: pool_post)
    $("#pool_posts").html(@view.render().el)

  edit: (id) ->
    pool_post = @pool_posts.get(id)

    @view = new WebAdmin.Views.PoolPosts.EditView(model: pool_post)
    $("#pool_posts").html(@view.render().el)
