WebAdmin.Views.QueuePosts ||= {}

class WebAdmin.Views.QueuePosts.ShowView extends Backbone.View
  template: JST["backbone/templates/queue_posts/show"]

  render: ->
    $(@el).html(@template(@model.toJSON() ))
    return this
