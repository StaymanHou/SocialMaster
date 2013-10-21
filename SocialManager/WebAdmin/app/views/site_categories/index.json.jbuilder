json.array!(@site_categories) do |site_category|
  json.extract! site_category, :name
  json.url site_category_url(site_category, format: :json)
end
