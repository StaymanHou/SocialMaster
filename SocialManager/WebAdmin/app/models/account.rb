class Account < ActiveRecord::Base
	has_many :acc_settings, dependent: :destroy
	before_save :default_values
	after_create :chain_create

	private
		def default_values
			# self.deleted ||= false
			self.deleted = false if self.deleted.nil?
			true
		end

		def chain_create
			smodules = Smodule.all
			smodules.each do |smodule|
				acc_setting = AccSetting.new
				acc_setting.smodule = smodule
				acc_setting.account = self
				acc_setting.save
			end
		end
end
