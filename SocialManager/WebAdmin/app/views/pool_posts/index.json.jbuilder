json.array!(@pool_posts) do |pool_post|
  json.extract! pool_post, :account_id, :pool_post_type_id, :site_id, :hidden, :title, :description, :content, :tags, :image_file, :image_link, :link, :social_score, :created_at
  json.url pool_post_url(pool_post, format: :json)
end
