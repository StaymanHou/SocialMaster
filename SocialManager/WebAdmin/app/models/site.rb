class Site < ActiveRecord::Base
  belongs_to :site_category
  has_many :tags, dependent: :destroy
end
