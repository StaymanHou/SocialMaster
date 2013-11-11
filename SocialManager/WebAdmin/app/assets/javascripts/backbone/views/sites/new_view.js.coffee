WebAdmin.Views.Sites ||= {}

class WebAdmin.Views.Sites.NewView extends Backbone.View
  template: JST["backbone/templates/sites/new"]

  events:
    "submit #new-site": "save"

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
      success: (site) =>
        @model = site
        window.location.hash = "/#{@model.id}"

      error: (site, jqXHR) =>
        @model.set({errors: $.parseJSON(jqXHR.responseText)})
    )

  render: ->
    $(@el).html(@template(@model.toJSON() ))

    this.$("form").backboneLink(@model)

    return this
