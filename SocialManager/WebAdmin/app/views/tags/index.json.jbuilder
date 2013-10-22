json.array!(@tags) do |tag|
  json.extract! tag, :site_id, :str
  json.url tag_url(tag, format: :json)
end
