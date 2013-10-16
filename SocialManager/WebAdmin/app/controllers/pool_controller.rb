class PoolController < ApplicationController
	def rss
		@active_page = "RSS"
	end

	def web
		@active_page = "Web"
	end

	def social
		@active_page = "Social"
	end
end
