class WebAdmin.Routers.SitesRouter extends Backbone.Router
  initialize: (options) ->
    @sites = new WebAdmin.Collections.SitesCollection()
    @sites.reset options.sites

  routes:
    "new"      : "newSite"
    "index"    : "index"
    ":id/edit" : "edit"
    ":id"      : "show"
    ".*"        : "index"

  newSite: ->
    @view = new WebAdmin.Views.Sites.NewView(collection: @sites)
    $("#sites").html(@view.render().el)

  index: ->
    @view = new WebAdmin.Views.Sites.IndexView(sites: @sites)
    $("#sites").html(@view.render().el)

  show: (id) ->
    site = @sites.get(id)

    @view = new WebAdmin.Views.Sites.ShowView(model: site)
    $("#sites").html(@view.render().el)

  edit: (id) ->
    site = @sites.get(id)

    @view = new WebAdmin.Views.Sites.EditView(model: site)
    $("#sites").html(@view.render().el)
