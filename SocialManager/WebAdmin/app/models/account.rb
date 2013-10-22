class Account < ActiveRecord::Base
  has_many :acc_settings
  has_many :pool_posts
end
