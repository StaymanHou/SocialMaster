WebAdmin.Views.PoolPosts ||= {}

class WebAdmin.Views.PoolPosts.PoolPostView extends Backbone.View
  template: JST["backbone/templates/pool_posts/pool_post"]

  events:
    'click div.pool-post': 'modal'
    'click a.hide-trigger': 'hide'
    'click .save-change': 'save_change'
    'click .forward-cell.twitter .link': 'twitter_link'
    'click .forward-cell.twitter .link-now': 'twitter_link_now'
    'click .forward-cell.twitter .image': 'twitter_image'
    'click .forward-cell.twitter .image-now': 'twitter_image_now'
    'click .forward-cell.twitter .manual': 'twitter_manual'
    'click .forward-cell.facebook .link': 'facebook_link'
    'click .forward-cell.facebook .link-now': 'facebook_link_now'
    'click .forward-cell.facebook .image': 'facebook_image'
    'click .forward-cell.facebook .image-now': 'facebook_image_now'
    'click .forward-cell.facebook .manual': 'facebook_manual'
    'click .forward-cell.gplus .link': 'gplus_link'
    'click .forward-cell.gplus .link-now': 'gplus_link_now'
    'click .forward-cell.gplus .image': 'gplus_image'
    'click .forward-cell.gplus .image-now': 'gplus_image_now'
    'click .forward-cell.gplus .manual': 'gplus_manual'
    'click .forward-cell.tumblr .link': 'tumblr_link'
    'click .forward-cell.tumblr .link-now': 'tumblr_link_now'
    'click .forward-cell.tumblr .image': 'tumblr_image'
    'click .forward-cell.tumblr .image-now': 'tumblr_image_now'
    'click .forward-cell.tumblr .manual': 'tumblr_manual'
    'click .forward-cell.pinterest .image': 'pinterest_image'
    'click .forward-cell.pinterest .image-now': 'pinterest_image_now'
    'click .forward-cell.pinterest .manual': 'pinterest_manual'

  tagName: "tr"

  modal: ->
    $('#myModal'+@model.get('id')).modal()

  hide: ->
    @model.hide()
    @$el.remove()

    return false

  save_change: ->
    @model.set('account_id', @.$('.pool_post_account_id').val())
    @model.set('pool_post_type_id', @.$('.pool_post_pool_post_type_id').val())
    @model.set('site_id', @.$('.pool_post_site_id').val())
    @model.set('title', @.$('.pool_post_title').val())
    @model.set('description', @.$('.pool_post_description').val())
    @model.set('content', @.$('.pool_post_content').val())
    @model.set('tags', @.$('.pool_post_tags').val())
    @model.set('image_file', @.$('.pool_post_image_file').val())
    @model.set('image_link', @.$('.pool_post_image_link').val())
    @model.set('link', @.$('.pool_post_link').val())
    @model.set('social_score', @.$('.pool_post_social_score').val())

    $('#myModal'+@model.get('id')).modal('hide')

    @model.save(null,
      success: (pool_post) =>
        @.$('.pool-post > p:first-child').html(pool_post.get('title'))
        @.$('.pool-post img').attr('src', '../images/postimg/rss/'+pool_post.get('image_file'))
        @.$('.modal img').attr('src', '../images/postimg/rss/'+pool_post.get('image_file'))
        $('.onpage-alert').html('Change saved!')

      error: (pool_post, jqXHR) =>
        $('.onpage-alert').html($.parseJSON(jqXHR.responseText))
    )
    
    $('.onpage-alert').show()

    return false

  push_queue_number: (smodule) ->
    count = $('th.'+smodule+'header').data('count')
    count += 1
    $('th.'+smodule+'header').data('count', count)
    $('th.'+smodule+'header span').html(count)
    @check_all_posted()

  check_all_posted: ->
    all_posted_flag = true
    cells = @.$('.forward-cell')
    cells.each ->
      if not $(@).hasClass('posted')
        all_posted_flag = false
    if all_posted_flag
      @hide()

  proto_queue_post: (smodule, post_type_id, content, schedule_time) ->
    if schedule_time == 'now'
      d = new Date
      schedule_time = (d.getFullYear()) + '/' + (d.getMonth()+1) + '/' + (d.getDate()) + ' ' + (d.getHours()) + ':' + (d.getMinutes()) + ':' + (d.getSeconds())
    image_file = null
    image_link = null
    if post_type_id == 2
      image_file = @model.get('image_file')
      image_link = @model.get('image_link')
    queuePost = new WebAdmin.Models.QueuePost
      status_id: 1
      acc_setting_id: @options.accsettingsti[smodule]['id']
      pool_post_id: @model.id
      post_type: post_type_id
      title: @model.get('title')
      content: content
      extra_content: @options.accsettingsti[smodule]['extra_content']
      tags: @model.get('tags')
      image_file: image_file
      image_link: image_link
      link: @model.get('link')
      other_field: @options.accsettingsti[smodule]['other_setting']
      schedule_time: schedule_time

    myself = @
    queuePost.save(null,
      success: ->
        $('.onpage-alert').html('Link '+smodule)
        myself.$('.forward-cell.'+smodule).addClass('posted').html('<div>posted</div>')
        myself.push_queue_number(smodule)

      error: ->
        $('.onpage-alert').html('Link '+smodule+' failed')
    )

    $('.onpage-alert').show()
    return false

  twitter_link: ->
    @proto_queue_post('twitter', 1, null, null)
    return false

  twitter_link_now: ->
    @proto_queue_post('twitter', 1, null, 'now')
    return false

  twitter_image: ->
    @proto_queue_post('twitter', 2, null, null)
    return false

  twitter_image_now: ->
    @proto_queue_post('twitter', 2, null, 'now')
    return false

  twitter_manual: ->
    ptype = 1
    ptype = 2 if @model.get('image_file')
    queuePost = new WebAdmin.Models.QueuePost
      status_id: 1
      acc_setting_id: @options.accsettingsti['twitter']['id']
      pool_post_id: @model.id
      post_type: ptype
      title: @model.get('title')
      content: null
      extra_content: @options.accsettingsti['twitter']['extra_content']
      tags: @model.get('tags')
      image_file: @model.get('image_file')
      image_link: @model.get('image_link')
      link: @model.get('link')
      other_field: @options.accsettingsti['twitter']['other_setting']
      schedule_time: null

    queuePostView = new WebAdmin.Views.QueuePosts.QueuePostView
      model: queuePost
      parent: @
      smodule: 'twitter'

    $('#ManualModal').html(queuePostView.render().el)
    $('#ManualModal').modal()
    return false

  facebook_link: ->
    @proto_queue_post('facebook', 1, @model.get('title'), null)
    return false

  facebook_link_now: ->
    @proto_queue_post('facebook', 1, @model.get('title'), 'now')
    return false

  facebook_image: ->
    @proto_queue_post('facebook', 2, @model.get('title'), null)
    return false

  facebook_image_now: ->
    @proto_queue_post('facebook', 2, @model.get('title'), 'now')
    return false

  facebook_manual: ->
    ptype = 1
    ptype = 2 if @model.get('image_file')
    queuePost = new WebAdmin.Models.QueuePost
      status_id: 1
      acc_setting_id: @options.accsettingsti['facebook']['id']
      pool_post_id: @model.id
      post_type: ptype
      title: @model.get('title')
      content: null
      extra_content: @options.accsettingsti['facebook']['extra_content']
      tags: @model.get('tags')
      image_file: @model.get('image_file')
      image_link: @model.get('image_link')
      link: @model.get('link')
      other_field: @options.accsettingsti['facebook']['other_setting']
      schedule_time: null

    queuePostView = new WebAdmin.Views.QueuePosts.QueuePostView
      model: queuePost
      parent: @
      smodule: 'facebook'

    $('#ManualModal').html(queuePostView.render().el)
    $('#ManualModal').modal()
    return false

  gplus_link: ->
    @proto_queue_post('gplus', 1, @model.get('title'), null)
    return false

  gplus_link_now: ->
    @proto_queue_post('gplus', 1, @model.get('title'), 'now')
    return false

  gplus_image: ->
    @proto_queue_post('gplus', 2, @model.get('title'), null)
    return false

  gplus_image_now: ->
    @proto_queue_post('gplus', 2, @model.get('title'), 'now')
    return false

  gplus_manual: ->
    ptype = 1
    ptype = 2 if @model.get('image_file')
    queuePost = new WebAdmin.Models.QueuePost
      status_id: 1
      acc_setting_id: @options.accsettingsti['gplus']['id']
      pool_post_id: @model.id
      post_type: ptype
      title: @model.get('title')
      content: null
      extra_content: @options.accsettingsti['gplus']['extra_content']
      tags: @model.get('tags')
      image_file: @model.get('image_file')
      image_link: @model.get('image_link')
      link: @model.get('link')
      other_field: @options.accsettingsti['gplus']['other_setting']
      schedule_time: null

    queuePostView = new WebAdmin.Views.QueuePosts.QueuePostView
      model: queuePost
      parent: @
      smodule: 'gplus'

    $('#ManualModal').html(queuePostView.render().el)
    $('#ManualModal').modal()
    return false

  tumblr_link: ->
    @proto_queue_post('tumblr', 1, @model.get('description'), null)
    return false

  tumblr_link_now: ->
    @proto_queue_post('tumblr', 1, @model.get('description'), 'now')
    return false

  tumblr_image: ->
    @proto_queue_post('tumblr', 2, @model.get('description'), null)
    return false

  tumblr_image_now: ->
    @proto_queue_post('tumblr', 2, @model.get('description'), 'now')
    return false

  tumblr_manual: ->
    ptype = 1
    ptype = 2 if @model.get('image_file')
    queuePost = new WebAdmin.Models.QueuePost
      status_id: 1
      acc_setting_id: @options.accsettingsti['tumblr']['id']
      pool_post_id: @model.id
      post_type: ptype
      title: @model.get('title')
      content: null
      extra_content: @options.accsettingsti['tumblr']['extra_content']
      tags: @model.get('tags')
      image_file: @model.get('image_file')
      image_link: @model.get('image_link')
      link: @model.get('link')
      other_field: @options.accsettingsti['tumblr']['other_setting']
      schedule_time: null

    queuePostView = new WebAdmin.Views.QueuePosts.QueuePostView
      model: queuePost
      parent: @
      smodule: 'tumblr'

    $('#ManualModal').html(queuePostView.render().el)
    $('#ManualModal').modal()
    return false

  pinterest_image: ->
    @proto_queue_post('pinterest', 2, @model.get('description'), null)
    return false

  pinterest_image_now: ->
    @proto_queue_post('pinterest', 2, @model.get('description'), 'now')
    return false

  pinterest_manual: ->
    ptype = 1
    ptype = 2 if @model.get('image_file')
    queuePost = new WebAdmin.Models.QueuePost
      status_id: 1
      acc_setting_id: @options.accsettingsti['pinterest']['id']
      pool_post_id: @model.id
      post_type: ptype
      title: @model.get('title')
      content: null
      extra_content: @options.accsettingsti['pinterest']['extra_content']
      tags: @model.get('tags')
      image_file: @model.get('image_file')
      image_link: @model.get('image_link')
      link: @model.get('link')
      other_field: @options.accsettingsti['pinterest']['other_setting']
      schedule_time: null

    queuePostView = new WebAdmin.Views.QueuePosts.QueuePostView
      model: queuePost
      parent: @
      smodule: 'pinterest'

    $('#ManualModal').html(queuePostView.render().el)
    $('#ManualModal').modal()
    return false

  render: ->
    $(@el).html(@template($.extend({sites: @options.sitelist}, @model.toJSON()) ))
    return this
