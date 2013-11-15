WebAdmin.Views.QueuePosts ||= {}

class WebAdmin.Views.QueuePosts.QueuePostView extends Backbone.View
  template: JST["backbone/templates/queue_posts/queue_post"]

  events:
    "click .create" : "create"

  tagName: "tr"

  create: () ->
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

    $('#ManualModal').modal('hide')

    myparent = @options.parent
    mysmodule = @options.smodule
    @model.save(null,
      success: (queue_post) =>
        myparent.push_queue_number(mysmodule)
        $('.onpage-alert').html('Manual '+mysmodule)
        myparent.$('.forward-cell.'+mysmodule).addClass('posted').html('<div>posted</div>')

      error: (queue_post, jqXHR) =>
        $('.onpage-alert').html($.parseJSON(jqXHR.responseText))
    )
    
    $('.onpage-alert').show()

    return false

  render: ->
    $(@el).html(@template(@model.toJSON() ))
    return this
