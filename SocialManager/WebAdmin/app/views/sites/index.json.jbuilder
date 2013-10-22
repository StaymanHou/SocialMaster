json.array!(@sites) do |site|
  json.extract! site, :site_category_id, :domain
  json.url site_url(site, format: :json)
end
