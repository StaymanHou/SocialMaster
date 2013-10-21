class AutoModesController < ApplicationController
  before_action :set_auto_mode, only: [:show, :edit, :update, :destroy]

  # GET /auto_modes
  # GET /auto_modes.json
  def index
    @auto_modes = AutoMode.all
  end

  # GET /auto_modes/1
  # GET /auto_modes/1.json
  def show
  end

  # GET /auto_modes/new
  def new
    @auto_mode = AutoMode.new
  end

  # GET /auto_modes/1/edit
  def edit
  end

  # POST /auto_modes
  # POST /auto_modes.json
  def create
    @auto_mode = AutoMode.new(auto_mode_params)

    respond_to do |format|
      if @auto_mode.save
        format.html { redirect_to @auto_mode, notice: 'Auto mode was successfully created.' }
        format.json { render action: 'show', status: :created, location: @auto_mode }
      else
        format.html { render action: 'new' }
        format.json { render json: @auto_mode.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /auto_modes/1
  # PATCH/PUT /auto_modes/1.json
  def update
    respond_to do |format|
      if @auto_mode.update(auto_mode_params)
        format.html { redirect_to @auto_mode, notice: 'Auto mode was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @auto_mode.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /auto_modes/1
  # DELETE /auto_modes/1.json
  def destroy
    @auto_mode.destroy
    respond_to do |format|
      format.html { redirect_to auto_modes_url }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_auto_mode
      @auto_mode = AutoMode.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def auto_mode_params
      params.require(:auto_mode).permit(:title)
    end
end
