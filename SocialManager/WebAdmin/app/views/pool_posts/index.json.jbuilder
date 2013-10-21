json.array!(@pool_posts) do |pool_post|
  json.extract! pool_post, :hidden, :title, :description, :content, :tags, :image_file, :image_link, :link, :social_score
  json.url pool_post_url(pool_post, format: :json)
end
