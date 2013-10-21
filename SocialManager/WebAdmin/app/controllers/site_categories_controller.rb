class SiteCategoriesController < ApplicationController
  before_action :set_site_category, only: [:show, :edit, :update, :destroy]

  # GET /site_categories
  # GET /site_categories.json
  def index
    @site_categories = SiteCategory.all
  end

  # GET /site_categories/1
  # GET /site_categories/1.json
  def show
  end

  # GET /site_categories/new
  def new
    @site_category = SiteCategory.new
  end

  # GET /site_categories/1/edit
  def edit
  end

  # POST /site_categories
  # POST /site_categories.json
  def create
    @site_category = SiteCategory.new(site_category_params)

    respond_to do |format|
      if @site_category.save
        format.html { redirect_to @site_category, notice: 'Site category was successfully created.' }
        format.json { render action: 'show', status: :created, location: @site_category }
      else
        format.html { render action: 'new' }
        format.json { render json: @site_category.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /site_categories/1
  # PATCH/PUT /site_categories/1.json
  def update
    respond_to do |format|
      if @site_category.update(site_category_params)
        format.html { redirect_to @site_category, notice: 'Site category was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @site_category.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /site_categories/1
  # DELETE /site_categories/1.json
  def destroy
    @site_category.destroy
    respond_to do |format|
      format.html { redirect_to site_categories_url }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_site_category
      @site_category = SiteCategory.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def site_category_params
      params.require(:site_category).permit(:name)
    end
end
