WebAdmin.Views.PoolPosts ||= {}

class WebAdmin.Views.PoolPosts.PoolPostView extends Backbone.View
  template: JST["backbone/templates/pool_posts/pool_post"]


  events:
    'click div.pool-post': 'modal'
    'click a.hide-trigger': 'hide'
    'click .save-change': 'save_change'

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
        @.$('.pool-post p:first-child').html(pool_post.get('title'))
        @.$('.pool-post img').attr('src', '../images/postimg/rss/'+pool_post.get('image_file'))
        @.$('.modal img').attr('src', '../images/postimg/rss/'+pool_post.get('image_file'))
        $('.onpage-alert').html('Change saved!')

      error: (pool_post, jqXHR) =>
        $('.onpage-alert').html($.parseJSON(jqXHR.responseText))
    )
    
    $('.onpage-alert').show()

    return false

  render: ->
    $(@el).html(@template(@model.toJSON() ))
    return this
