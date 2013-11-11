class PoolController < ApplicationController
	def rss
		@active_page = "RSS"
		@accounts = Account.all
		@account_id = account_param[:account].to_i
		if @account_id != 0
			@account = Account.find(@account_id)
			@smodules = Smodule.all
		end
		@sites = Site.all
	end

	def web
		@active_page = "Web"
	end

	def social
		@active_page = "Social"
	end

	private
	    def account_param
    		params.permit(:account)
    	end
end
