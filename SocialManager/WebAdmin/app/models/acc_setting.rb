class AccSetting < ActiveRecord::Base
  belongs_to :account
  belongs_to :smodule
  belongs_to :auto_mode
  has_many :queue_posts
  has_many :post_data
  before_create :default_values

  private
  	def default_values
  	  self.other_setting = '{}'
  	  self.active = false
  	  self.auto_mode_id = 1
  	  self.time_start = DateTime.parse("00:00:00")
  	  self.time_end = DateTime.parse("00:00:00")
  	  self.num_per_day = 24
  	  self.min_post_interval = 60
  	  self.queue_size = 24
  	end

end
