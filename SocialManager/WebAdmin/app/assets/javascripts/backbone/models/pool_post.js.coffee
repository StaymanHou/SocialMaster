class WebAdmin.Models.PoolPost extends Backbone.Model
  paramRoot: 'pool_post'

  defaults:
    account_id: null
    pool_post_type_id: null
    site_id: null
    hidden: null
    title: null
    description: null
    content: null
    tags: null
    image_file: null
    image_link: null
    link: null
    social_score: null
    created_at: null

  hide: ->
    @set
      'hidden': true
    @save()

class WebAdmin.Collections.PoolPostsCollection extends Backbone.Collection
  model: WebAdmin.Models.PoolPost
  url: '/pool_posts'
