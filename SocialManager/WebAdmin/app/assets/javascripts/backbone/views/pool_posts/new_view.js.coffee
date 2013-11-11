WebAdmin.Views.PoolPosts ||= {}

class WebAdmin.Views.PoolPosts.NewView extends Backbone.View
  template: JST["backbone/templates/pool_posts/new"]

  events:
    "submit #new-pool_post": "save"

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
      success: (pool_post) =>
        @model = pool_post
        window.location.hash = "/#{@model.id}"

      error: (pool_post, jqXHR) =>
        @model.set({errors: $.parseJSON(jqXHR.responseText)})
    )

  render: ->
    $(@el).html(@template(@model.toJSON() ))

    this.$("form").backboneLink(@model)

    return this
