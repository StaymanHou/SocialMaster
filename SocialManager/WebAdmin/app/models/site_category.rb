class SiteCategory < ActiveRecord::Base
  has_many :sites, dependent: :destroy
end
