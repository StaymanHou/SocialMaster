json.array!(@acc_settings) do |acc_setting|
  json.extract! acc_setting, :username, :password, :other_setting, :extra_content, :active, :time_start, :time_end, :num_per_day, :min_post_interval, :queue_size
  json.url acc_setting_url(acc_setting, format: :json)
end
