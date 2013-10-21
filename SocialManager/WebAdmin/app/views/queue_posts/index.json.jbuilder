json.array!(@queue_posts) do |queue_post|
  json.extract! queue_post, :type, :title, :content, :extra_content, :tags, :image_file, :image_file, :link, :other_field, :schedule_time
  json.url queue_post_url(queue_post, format: :json)
end
