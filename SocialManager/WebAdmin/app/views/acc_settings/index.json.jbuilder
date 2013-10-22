json.array!(@acc_settings) do |acc_setting|
  json.extract! acc_setting, :account_id, :smodule_id, :username, :password, :other_setting, :extra_content, :active, :auto_mode_id, :time_start, :time_end, :num_per_day, :min_post_interval, :queue_size
  json.url acc_setting_url(acc_setting, format: :json)
end
