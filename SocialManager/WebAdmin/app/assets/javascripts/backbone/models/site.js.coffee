class WebAdmin.Models.Site extends Backbone.Model
  paramRoot: 'site'

  defaults:
    site_category_id: null
    domain: null

class WebAdmin.Collections.SitesCollection extends Backbone.Collection
  model: WebAdmin.Models.Site
  url: '/sites'
