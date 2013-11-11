WebAdmin.Views.PoolPosts ||= {}

class WebAdmin.Views.PoolPosts.EditView extends Backbone.View
  template : JST["backbone/templates/pool_posts/edit"]

  events :
    "submit #edit-pool_post" : "update"

  update : (e) ->
    e.preventDefault()
    e.stopPropagation()

    @model.save(null,
      success : (pool_post) =>
        @model = pool_post
        window.location.hash = "/#{@model.id}"
    )

  render : ->
    $(@el).html(@template(@model.toJSON() ))

    this.$("form").backboneLink(@model)

    return this
