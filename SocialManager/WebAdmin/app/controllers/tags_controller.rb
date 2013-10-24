class TagsController < ApplicationController
  before_action :init
  before_action :set_tag, only: [:show, :edit, :update, :destroy]

  # GET /tags
  # GET /tags.json
  def index
    @site_categories = SiteCategory.all
    @site_count = Site.count
    @tag_count = Tag.count
  end

  # GET /tags/1
  # GET /tags/1.json
  def show
  end

  # GET /tags/new
  def new
    @tag = Tag.new(params.permit(:site_id))
  end

  # GET /tags/1/edit
  def edit
  end

  # POST /tags
  # POST /tags.json
  def create
    @tag = Tag.new(tag_params)

    respond_to do |format|
      if @tag.save
        format.html {
          flash[:notice] = 'Tag was successfully created.'
          redirect_to @tag.site
        }
        format.json { render action: 'show', status: :created, location: @tag }
      else
        format.html { render action: 'new' }
        format.json { render json: @tag.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /tags/1
  # PATCH/PUT /tags/1.json
  def update
    respond_to do |format|
      if @tag.update(tag_params)
        format.html {
          flash[:notice] = 'Tag was successfully updated.'
          redirect_to @tag.site
        }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @tag.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /tags/1
  # DELETE /tags/1.json
  def destroy
    @tag.destroy
    respond_to do |format|
      format.html {
        flash[:notice] = 'Tag: %s was successfully removed.' % @tag.str
        redirect_to @tag.site
      }
      format.json { head :no_content }
    end
  end

  private
    # Executed as initializing
    def init
      @active_page = "Tags"
      @message = "test"
    end

    # Use callbacks to share common setup or constraints between actions.
    def set_tag
      @tag = Tag.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def tag_params
      params.require(:tag).permit(:site_id, :str)
    end
end
