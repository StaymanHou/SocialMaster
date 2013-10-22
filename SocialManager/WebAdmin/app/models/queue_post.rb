class QueuePost < ActiveRecord::Base
  belongs_to :status
  belongs_to :acc_setting
  belongs_to :rss_post
end
