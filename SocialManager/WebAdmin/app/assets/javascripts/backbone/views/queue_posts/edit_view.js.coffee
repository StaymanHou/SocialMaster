WebAdmin.Views.QueuePosts ||= {}

class WebAdmin.Views.QueuePosts.EditView extends Backbone.View
  template : JST["backbone/templates/queue_posts/edit"]

  events :
    "submit #edit-queue_post" : "update"

  update : (e) ->
    e.preventDefault()
    e.stopPropagation()

    @model.save(null,
      success : (queue_post) =>
        @model = queue_post
        window.location.hash = "/#{@model.id}"
    )

  render : ->
    $(@el).html(@template(@model.toJSON() ))

    this.$("form").backboneLink(@model)

    return this
