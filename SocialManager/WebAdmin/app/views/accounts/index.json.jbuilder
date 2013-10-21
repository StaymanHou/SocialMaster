json.array!(@accounts) do |account|
  json.extract! account, :name, :rss_urls, :active, :last_update, :deleted
  json.url account_url(account, format: :json)
end
