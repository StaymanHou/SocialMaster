json.array!(@sites) do |site|
  json.extract! site, :domain
  json.url site_url(site, format: :json)
end
