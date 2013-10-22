class QueuePost < ActiveRecord::Base
  belongs_to :status
  belongs_to :acc_setting
  belongs_to :pool_post
end
