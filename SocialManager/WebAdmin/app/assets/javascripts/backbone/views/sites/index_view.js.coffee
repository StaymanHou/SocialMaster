WebAdmin.Views.Sites ||= {}

class WebAdmin.Views.Sites.IndexView extends Backbone.View
  template: JST["backbone/templates/sites/index"]

  initialize: () ->
    @options.sites.bind('reset', @addAll)

  addAll: () =>
    @options.sites.each(@addOne)

  addOne: (site) =>
    view = new WebAdmin.Views.Sites.SiteView({model : site})
    @$("tbody").append(view.render().el)

  render: =>
    $(@el).html(@template(sites: @options.sites.toJSON() ))
    @addAll()

    return this
