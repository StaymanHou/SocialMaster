WebAdmin.Views.QueuePosts ||= {}

class WebAdmin.Views.QueuePosts.QueuePostWaterfallView extends Backbone.View
  template: JST["backbone/templates/queue_posts/queue_post_waterfall"]

  events:
    'click .queue-post': 'modal'
    'click .save-change': 'save_change'
    "click .destroy" : "destroy"

  tagName: "div"

  modal: ->
    $('#myModal'+@model.get('id')).modal()

    return false

  save_change: ->
    @model.set('status_id', @.$('.queue_post_status_id').val())
    @model.set('acc_setting_id', @.$('.queue_post_acc_setting_id').val())
    @model.set('pool_post_id', @.$('.queue_post_pool_post_id').val())
    @model.set('post_type', @.$('.queue_post_post_type').val())
    @model.set('title', @.$('.queue_post_title').val())
    @model.set('content', @.$('.queue_post_content').val())
    @model.set('extra_content', @.$('.queue_post_extra_content').val())
    @model.set('tags', @.$('.queue_post_tags').val())
    @model.set('image_file', @.$('.queue_post_image_file').val())
    @model.set('image_link', @.$('.queue_post_image_link').val())
    @model.set('link', @.$('.queue_post_link').val())
    @model.set('other_field', @.$('.queue_post_other_field').val())
    @model.set('schedule_time', @.$('.queue_post_schedule_time').val())

    $('#myModal'+@model.get('id')).modal('hide')

    that = @

    @model.save(null,
      success: (queue_post) ->
        that.$('.queue-post > p:first-child').html(queue_post.get('title'))
        that.$('.queue-post img').attr('src', '../images/postimg/rss/'+queue_post.get('image_file'))
        that.$('.modal img').attr('src', '../images/postimg/rss/'+queue_post.get('image_file'))
        $('.onpage-alert').html('Post change saved')
      error: (queue_post, jqXHR) ->
        $('.onpage-alert').html($.parseJSON(jqXHR.responseText))
    )

    $('.onpage-alert').show()

    return false

  destroy: () ->
    myparent = @options.parent
    mysmodule = @options.smodule
    @model.destroy
      success: (queue_post) ->
        myparent.pop_queue_number(mysmodule)
        $('.onpage-alert').html('Post deleted')
      error: (queue_post, jqXHR) ->
        $('.onpage-alert').html($.parseJSON(jqXHR.responseText))

    this.remove()
    count = $('#accordionacc .waterfall-header.'+@options.smodule.name+'header').data('count')
    count--
    $('#accordionacc .waterfall-header.'+@options.smodule.name+'header').data('count', count)

    $('.onpage-alert').show()

    return false

  render: ->
    $(@el).attr('status', @model.get('status_id')).html(@template(@model.toJSON() ))
    return this
