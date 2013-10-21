class AccSettingsController < ApplicationController
  before_action :set_acc_setting, only: [:show, :edit, :update, :destroy]

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
      if @acc_setting.update(acc_setting_params)
        format.html { redirect_to @acc_setting, notice: 'Acc setting was successfully updated.' }
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

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_acc_setting
      @acc_setting = AccSetting.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def acc_setting_params
      params.require(:acc_setting).permit(:username, :password, :other_setting, :extra_content, :active, :time_start, :time_end, :num_per_day, :min_post_interval, :queue_size)
    end
end
