class Account < ActiveRecord::Base
	has_many :acc_settings, dependent: :destroy
	before_save :default_values
	def default_values
		# self.deleted ||= false
		self.deleted = false if self.deleted.nil?
		true
	end
end
