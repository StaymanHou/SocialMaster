class AccSetting < ActiveRecord::Base
  belongs_to :account
  belongs_to :smodule
  belongs_to :auto_mode
end
