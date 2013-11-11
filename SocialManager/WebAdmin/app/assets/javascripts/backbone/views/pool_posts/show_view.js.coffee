WebAdmin.Views.PoolPosts ||= {}

class WebAdmin.Views.PoolPosts.ShowView extends Backbone.View
  template: JST["backbone/templates/pool_posts/show"]

  render: ->
    $(@el).html(@template(@model.toJSON() ))
    return this
