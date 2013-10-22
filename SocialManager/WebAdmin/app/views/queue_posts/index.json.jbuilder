json.array!(@queue_posts) do |queue_post|
  json.extract! queue_post, :status_id, :acc_setting_id, :pool_post_id, :type, :title, :content, :extra_content, :tags, :image_file, :link, :other_field, :schedule_time
  json.url queue_post_url(queue_post, format: :json)
end
