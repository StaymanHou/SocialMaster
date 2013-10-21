class PoolPostTypesController < ApplicationController
  before_action :set_pool_post_type, only: [:show, :edit, :update, :destroy]

  # GET /pool_post_types
  # GET /pool_post_types.json
  def index
    @pool_post_types = PoolPostType.all
  end

  # GET /pool_post_types/1
  # GET /pool_post_types/1.json
  def show
  end

  # GET /pool_post_types/new
  def new
    @pool_post_type = PoolPostType.new
  end

  # GET /pool_post_types/1/edit
  def edit
  end

  # POST /pool_post_types
  # POST /pool_post_types.json
  def create
    @pool_post_type = PoolPostType.new(pool_post_type_params)

    respond_to do |format|
      if @pool_post_type.save
        format.html { redirect_to @pool_post_type, notice: 'Pool post type was successfully created.' }
        format.json { render action: 'show', status: :created, location: @pool_post_type }
      else
        format.html { render action: 'new' }
        format.json { render json: @pool_post_type.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /pool_post_types/1
  # PATCH/PUT /pool_post_types/1.json
  def update
    respond_to do |format|
      if @pool_post_type.update(pool_post_type_params)
        format.html { redirect_to @pool_post_type, notice: 'Pool post type was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @pool_post_type.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /pool_post_types/1
  # DELETE /pool_post_types/1.json
  def destroy
    @pool_post_type.destroy
    respond_to do |format|
      format.html { redirect_to pool_post_types_url }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_pool_post_type
      @pool_post_type = PoolPostType.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def pool_post_type_params
      params.require(:pool_post_type).permit(:title)
    end
end
