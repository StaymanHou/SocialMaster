class WebAdmin.Models.QueuePost extends Backbone.Model
  paramRoot: 'queue_post'
  urlRoot: '/queue_posts'

  defaults:
    status_id: null
    acc_setting_id: null
    pool_post_id: null
    post_type: null
    title: null
    content: null
    extra_content: null
    tags: null
    image_file: null
    image_link: null
    link: null
    other_field: null
    schedule_time: null

class WebAdmin.Collections.QueuePostsCollection extends Backbone.Collection
  model: WebAdmin.Models.QueuePost
  url: '/queue_posts'
