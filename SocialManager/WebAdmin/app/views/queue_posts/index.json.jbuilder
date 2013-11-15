json.array!(@queue_posts) do |queue_post|
  json.extract! queue_post, :id, :status_id, :acc_setting_id, :pool_post_id, :post_type, :title, :content, :extra_content, :tags, :image_file, :image_link, :link, :other_field, :schedule_time
  json.url queue_post_url(queue_post, format: :json)
end
