json.array!(@tags) do |tag|
  json.extract! tag, :str
  json.url tag_url(tag, format: :json)
end
