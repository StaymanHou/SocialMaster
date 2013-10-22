class Site < ActiveRecord::Base
  belongs_to :site_category
  has_many :pool_posts
end
