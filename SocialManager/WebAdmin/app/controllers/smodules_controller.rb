class SmodulesController < ApplicationController
  before_action :init
  before_action :set_smodule, only: [:show, :edit, :update, :destroy]

  # GET /smodules
  # GET /smodules.json
  def index
    @smodules = Smodule.all
  end

  # GET /smodules/1
  # GET /smodules/1.json
  def show
  end

  # GET /smodules/new
  def new
    @smodule = Smodule.new
  end

  # GET /smodules/1/edit
  def edit
  end

  # POST /smodules
  # POST /smodules.json
  def create
    @smodule = Smodule.new(smodule_params)

    respond_to do |format|
      if @smodule.save
        format.html {
          flash[:notice] = 'Module was successfully created.'
          redirect_to smodules_url
        }
        format.json { render action: 'show', status: :created, location: @smodule }
      else
        format.html { render action: 'new' }
        format.json { render json: @smodule.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /smodules/1
  # PATCH/PUT /smodules/1.json
  def update
    respond_to do |format|
      if @smodule.update(smodule_params)
        format.html { redirect_to @smodule, notice: 'Smodule was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @smodule.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /smodules/1
  # DELETE /smodules/1.json
  def destroy
    @smodule.destroy
    respond_to do |format|
      format.html {
        flash[:notice] = 'Module: %s was successfully removed.' % @smodule.name
        redirect_to smodules_url
      }
      format.json { head :no_content }
    end
  end

  private
    # Executed as initializing
    def init
      @active_page = "Modules"
    end

    # Use callbacks to share common setup or constraints between actions.
    def set_smodule
      @smodule = Smodule.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def smodule_params
      params.require(:smodule).permit(:name)
    end
end
