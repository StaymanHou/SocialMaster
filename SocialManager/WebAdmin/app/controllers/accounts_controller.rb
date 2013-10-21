class AccountsController < ApplicationController
	def initialize
		super
		@active_page = "Accounts"
		@message = "test"
	end
	def index
		
	end
	def new
		
	end
	def create
		
	end
	def edit
		
	end
	def update
		
	end
	def destroy
		@message = "Account: bala has been deleted!"
		redirect_to accounts_path
	end
	def toggle_active
		@message = "Account: bala has been activated!"
		redirect_to  accounts_path	
	end

	private
		def post_params
			params.require(:post).permit(:title, :text)
		end

end
