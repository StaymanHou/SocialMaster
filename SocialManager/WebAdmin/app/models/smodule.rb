class Smodule < ActiveRecord::Base
	has_many :acc_settings, dependent: :destroy
	after_create :chain_create

	private
		def chain_create
			accounts = Account.all
			accounts.each do |account|
				acc_setting = AccSetting.new
				acc_setting.smodule = self
				acc_setting.account = account
				acc_setting.save
			end
		end

end
