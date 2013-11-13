class HomeController < ApplicationController
	def index
		@active_page = "Home"
		@smodules = Smodule.all
		@smodules ||= []
		@sites = Site.all
		@sites ||= []
		@tag_count = Tag.count
		@active_accounts = Account.where(active: true)
		@active_accounts ||= []
		@accounts = Account.all
		@accounts ||= []
		@pool_post_types = PoolPostType.all
		@pool_post_types ||= []
		@statuses = Status.all
		@statuses ||= []

	end
end
