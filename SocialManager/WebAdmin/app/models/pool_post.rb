class PoolPost < ActiveRecord::Base
  belongs_to :account
  belongs_to :pool_post_type
  belongs_to :site
  has_many :queue_posts
end
