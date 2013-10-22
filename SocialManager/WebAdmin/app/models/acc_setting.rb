class AccSetting < ActiveRecord::Base
  belongs_to :account
  belongs_to :smodule
  belongs_to :auto_mode
  has_many :post_data
  has_many :queue_posts
end
