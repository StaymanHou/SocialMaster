class Status < ActiveRecord::Base
  has_many :queue_posts
end
