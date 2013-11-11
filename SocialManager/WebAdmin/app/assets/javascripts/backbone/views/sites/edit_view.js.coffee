WebAdmin.Views.Sites ||= {}

class WebAdmin.Views.Sites.EditView extends Backbone.View
  template : JST["backbone/templates/sites/edit"]

  events :
    "submit #edit-site" : "update"

  update : (e) ->
    e.preventDefault()
    e.stopPropagation()

    @model.save(null,
      success : (site) =>
        @model = site
        window.location.hash = "/#{@model.id}"
    )

  render : ->
    $(@el).html(@template(@model.toJSON() ))

    this.$("form").backboneLink(@model)

    return this
