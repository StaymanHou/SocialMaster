json.array!(@post_data) do |post_datum|
  json.extract! post_datum, :acc_setting_id, :type, :title, :content, :extra_content, :tags, :image_file, :link, :other_field, :data
  json.url post_datum_url(post_datum, format: :json)
end
