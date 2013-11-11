WebAdmin.Views.Sites ||= {}

class WebAdmin.Views.Sites.ShowView extends Backbone.View
  template: JST["backbone/templates/sites/show"]

  render: ->
    $(@el).html(@template(@model.toJSON() ))
    return this
