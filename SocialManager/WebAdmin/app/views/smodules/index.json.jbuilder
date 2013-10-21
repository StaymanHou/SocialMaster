json.array!(@smodules) do |smodule|
  json.extract! smodule, :name
  json.url smodule_url(smodule, format: :json)
end
