WebAdmin.Views.QueuePosts ||= {}

class WebAdmin.Views.QueuePosts.NewView extends Backbone.View
  template: JST["backbone/templates/queue_posts/new"]

  events:
    "submit #new-queue_post": "save"

  constructor: (options) ->
    super(options)
    @model = new @collection.model()

    @model.bind("change:errors", () =>
      this.render()
    )

  save: (e) ->
    e.preventDefault()
    e.stopPropagation()

    @model.unset("errors")

    @collection.create(@model.toJSON(),
      success: (queue_post) =>
        @model = queue_post
        window.location.hash = "/#{@model.id}"

      error: (queue_post, jqXHR) =>
        @model.set({errors: $.parseJSON(jqXHR.responseText)})
    )

  render: ->
    $(@el).html(@template(@model.toJSON() ))

    this.$("form").backboneLink(@model)

    return this
