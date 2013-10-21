class PostDataController < ApplicationController
  before_action :set_post_datum, only: [:show, :edit, :update, :destroy]

  # GET /post_data
  # GET /post_data.json
  def index
    @post_data = PostDatum.all
  end

  # GET /post_data/1
  # GET /post_data/1.json
  def show
  end

  # GET /post_data/new
  def new
    @post_datum = PostDatum.new
  end

  # GET /post_data/1/edit
  def edit
  end

  # POST /post_data
  # POST /post_data.json
  def create
    @post_datum = PostDatum.new(post_datum_params)

    respond_to do |format|
      if @post_datum.save
        format.html { redirect_to @post_datum, notice: 'Post datum was successfully created.' }
        format.json { render action: 'show', status: :created, location: @post_datum }
      else
        format.html { render action: 'new' }
        format.json { render json: @post_datum.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /post_data/1
  # PATCH/PUT /post_data/1.json
  def update
    respond_to do |format|
      if @post_datum.update(post_datum_params)
        format.html { redirect_to @post_datum, notice: 'Post datum was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @post_datum.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /post_data/1
  # DELETE /post_data/1.json
  def destroy
    @post_datum.destroy
    respond_to do |format|
      format.html { redirect_to post_data_url }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_post_datum
      @post_datum = PostDatum.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def post_datum_params
      params.require(:post_datum).permit(:type, :title, :content, :extra_content, :tags, :image_file, :link, :other_field, :data)
    end
end
