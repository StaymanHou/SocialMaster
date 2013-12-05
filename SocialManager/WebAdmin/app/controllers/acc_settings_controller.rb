class AccSettingsController < ApplicationController
  before_action :init
  before_action :set_acc_setting, only: [:show, :edit, :update, :destroy, :toggle_active]

  # GET /acc_settings
  # GET /acc_settings.json
  def index
    @acc_settings = AccSetting.all
  end

  # GET /acc_settings/1
  # GET /acc_settings/1.json
  def show
  end

  # GET /acc_settings/new
  def new
    @acc_setting = AccSetting.new
  end

  # GET /acc_settings/1/edit
  def edit
  end

  # POST /acc_settings
  # POST /acc_settings.json
  def create
    @acc_setting = AccSetting.new(acc_setting_params)

    respond_to do |format|
      if @acc_setting.save
        format.html { redirect_to @acc_setting, notice: 'Acc setting was successfully created.' }
        format.json { render action: 'show', status: :created, location: @acc_setting }
      else
        format.html { render action: 'new' }
        format.json { render json: @acc_setting.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /acc_settings/1
  # PATCH/PUT /acc_settings/1.json
  def update
    respond_to do |format|
      if @acc_setting.update(acc_setting_params_for_update)
        format.html {
          flash[:notice] = 'Account Setting was successfully updated.'
          redirect_to accounts_url
        }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @acc_setting.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /acc_settings/1
  # DELETE /acc_settings/1.json
  def destroy
    @acc_setting.destroy
    respond_to do |format|
      format.html { redirect_to acc_settings_url }
      format.json { head :no_content }
    end
  end

  # TOGGLE_ACTIVE /accounts/1/toggle_active
  def toggle_active
    respond_to do |format|
      if @acc_setting.update({active: !@acc_setting.active})
        format.html {
          if @acc_setting.active
            notice = 'Acc_setting: %s | %s has been activated' % [@acc_setting.account.name, @acc_setting.smodule.name]
          else
            notice = 'Acc_setting: %s | %s has been inactivated' % [@acc_setting.account.name, @acc_setting.smodule.name]
          end
          redirect_to accounts_url, flash: {notice: notice}
        }
        format.json { head :no_content }
      else
        format.html {
          redirect_to accounts_url, flash: {notice: @acc_setting.errors.full_messages.to_s}
        }
        format.json { render json: @acc_setting.errors, status: :unprocessable_entity }
      end
    end
  end

  private
    # Executed as initializing
    def init
      @active_page = "Accounts"
    end

    # Use callbacks to share common setup or constraints between actions.
    def set_acc_setting
      @acc_setting = AccSetting.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def acc_setting_params
      params.require(:acc_setting).permit(:username, :password, :other_setting, :extra_content, :active, :auto_mode_id, :time_start, :time_end, :num_per_day, :min_post_interval, :queue_size)
    end

    def acc_setting_params_for_update
      return acc_setting_params if params.require(:acc_setting)[:password].present?
      params.require(:acc_setting).permit(:username, :other_setting, :extra_content, :active, :auto_mode_id, :time_start, :time_end, :num_per_day, :min_post_interval, :queue_size)
    end
end
