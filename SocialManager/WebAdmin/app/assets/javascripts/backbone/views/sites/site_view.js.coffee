WebAdmin.Views.Sites ||= {}

class WebAdmin.Views.Sites.SiteView extends Backbone.View
  template: JST["backbone/templates/sites/site"]

  events:
    "click .destroy" : "destroy"

  tagName: "tr"

  destroy: () ->
    @model.destroy()
    this.remove()

    return false

  render: ->
    $(@el).html(@template(@model.toJSON() ))
    return this
