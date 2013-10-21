json.array!(@auto_modes) do |auto_mode|
  json.extract! auto_mode, :title
  json.url auto_mode_url(auto_mode, format: :json)
end
