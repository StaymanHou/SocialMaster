class QueueController < ApplicationController
	def index
		@active_page = "Queue"
		@accounts = Account.all
		@account_id = account_param.to_i
		if @account_id != 0
			@account = Account.find(@account_id)
			@smodules = Smodule.all
			acc_settings = AccSetting.where(account_id: @account_id)
			@accsettingsti = Hash.new
			acc_settings.each do |acc_setting|
				@accsettingsti[acc_setting.smodule.name] = acc_setting
			end
		end
	end

	private
		def account_param
			params[:account]
		end
end
