class AccountsController < ApplicationController
  before_action :init
  before_action :set_account, only: [:show, :edit, :update, :destroy, :toggle_active]

  # GET /accounts
  # GET /accounts.json
  def index
    @accounts = Account.all
    @smodules = Smodule.all
  end

  # GET /accounts/1
  # GET /accounts/1.json
  def show
  end

  # GET /accounts/new
  def new
    @account = Account.new
  end

  # GET /accounts/1/edit
  def edit
  end

  # POST /accounts
  # POST /accounts.json
  def create
    @account = Account.new(account_params)

    respond_to do |format|
      if @account.save
        format.html {
          flash[:notice] = 'Account was successfully created.'
          redirect_to accounts_url
        }
        format.json { render action: 'show', status: :created, location: @account }
      else
        format.html { render action: 'new' }
        format.json { render json: @account.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /accounts/1
  # PATCH/PUT /accounts/1.json
  def update
    respond_to do |format|
      if @account.update(account_params)
        format.html {
          flash[:notice] = 'Account was successfully updated.'
          redirect_to accounts_url
        }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @account.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /accounts/1
  # DELETE /accounts/1.json
  def destroy
    @account.destroy
    respond_to do |format|
      format.html {
        flash[:notice] = 'Account: blah has been deleted.'
        redirect_to accounts_url 
      }
      format.json { head :no_content }
    end
  end

  # TOGGLE_ACTIVE /accounts/1/toggle_active
  def toggle_active
    respond_to do |format|
      if @account.update({active: !@account.active})
        format.html {
          if @account.active
            notice = 'Account: %s has been activated' % @account.name
          else
            notice = 'Account: %s has been inactivated' % @account.name
          end
          redirect_to accounts_url, flash: {notice: notice}
        }
        format.json { head :no_content }
      else
        format.html {
          redirect_to accounts_url, flash: {notice: @account.errors.full_messages.to_s}
        }
        format.json { render json: @account.errors, status: :unprocessable_entity }
      end
    end
  end

  private
    # Executed as initializing
    def init
      @active_page = "Accounts"
    end

    # Use callbacks to share common setup or constraints between actions.
    def set_account
      @account = Account.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def account_params
      params.require(:account).permit(:name, :rss_urls, :active, :last_update, :deleted)
    end
end
