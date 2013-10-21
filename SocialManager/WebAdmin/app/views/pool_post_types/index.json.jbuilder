json.array!(@pool_post_types) do |pool_post_type|
  json.extract! pool_post_type, :title
  json.url pool_post_type_url(pool_post_type, format: :json)
end
