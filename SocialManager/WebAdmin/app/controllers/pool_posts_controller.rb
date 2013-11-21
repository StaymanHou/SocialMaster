class PoolPostsController < ApplicationController
  before_action :set_pool_post, only: [:show, :edit, :update, :destroy]
  include ApplicationHelper

  # GET /pool_posts
  # GET /pool_posts.json
  def index
    hidden = to_bool(params[:hidden])
    cursor = params[:cursor].to_i
    if cursor == 0
      @pool_posts = PoolPost.order("id DESC").where("account_id = ? AND hidden = ?", params[:account_id], hidden).limit(30)
    elsif cursor > 0
      @pool_posts = PoolPost.order("id DESC").where("account_id = ? AND hidden = ? AND id < ?", params[:account_id], hidden, cursor).limit(30)
    elsif cursor == -1
      @pool_posts = PoolPost.order("id ASC").where("account_id = ? AND hidden = ? AND id > ?", params[:account_id], hidden, params[:latest].to_i)
    end
  end

  # GET /pool_posts/1
  # GET /pool_posts/1.json
  def show
  end

  # GET /pool_posts/new
  def new
    @from = params[:from]
    @pool_post = PoolPost.new(new_params)
  end

  # GET /pool_posts/1/edit
  def edit
  end

  # POST /pool_posts
  # POST /pool_posts.json
  def create
    @pool_post = PoolPost.new(pool_post_params)
    @from = params[:from]

    if @from == 'rss'
      if @pool_post.account_id
        rt = pool_rss_path(account: @pool_post.account_id)
      else
        rt = pool_rss_path
      end
    elsif @from == 'web'
      rt = pool_web_path
    elsif @from == 'social'
      rt = pool_social_path
    else
      rt = home_index_path
    end

    respond_to do |format|
      if @pool_post.save
        format.html { redirect_to rt, notice: 'Pool post was successfully created.' }
        format.json { render action: 'show', status: :created, location: @pool_post }
      else
        format.html { render action: 'new' }
        format.json { render json: @pool_post.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /pool_posts/1
  # PATCH/PUT /pool_posts/1.json
  def update
    respond_to do |format|
      if @pool_post.update(pool_post_params)
        format.html { redirect_to @pool_post, notice: 'Pool post was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @pool_post.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /pool_posts/1
  # DELETE /pool_posts/1.json
  def destroy
    @pool_post.destroy
    respond_to do |format|
      format.html { redirect_to pool_posts_url }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_pool_post
      @pool_post = PoolPost.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def pool_post_params
      params.require(:pool_post).permit(:account_id, :pool_post_type_id, :site_id, :hidden, :title, :description, :content, :tags, :image_file, :image_link, :link, :social_score)
    end

    def new_params
      params.permit(:account_id, :pool_post_type_id)
    end
end
