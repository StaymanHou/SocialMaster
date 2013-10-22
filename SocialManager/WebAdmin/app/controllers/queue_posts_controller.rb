class QueuePostsController < ApplicationController
  before_action :set_queue_post, only: [:show, :edit, :update, :destroy]

  # GET /queue_posts
  # GET /queue_posts.json
  def index
    @queue_posts = QueuePost.all
  end

  # GET /queue_posts/1
  # GET /queue_posts/1.json
  def show
  end

  # GET /queue_posts/new
  def new
    @queue_post = QueuePost.new
  end

  # GET /queue_posts/1/edit
  def edit
  end

  # POST /queue_posts
  # POST /queue_posts.json
  def create
    @queue_post = QueuePost.new(queue_post_params)

    respond_to do |format|
      if @queue_post.save
        format.html { redirect_to @queue_post, notice: 'Queue post was successfully created.' }
        format.json { render action: 'show', status: :created, location: @queue_post }
      else
        format.html { render action: 'new' }
        format.json { render json: @queue_post.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /queue_posts/1
  # PATCH/PUT /queue_posts/1.json
  def update
    respond_to do |format|
      if @queue_post.update(queue_post_params)
        format.html { redirect_to @queue_post, notice: 'Queue post was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @queue_post.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /queue_posts/1
  # DELETE /queue_posts/1.json
  def destroy
    @queue_post.destroy
    respond_to do |format|
      format.html { redirect_to queue_posts_url }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_queue_post
      @queue_post = QueuePost.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def queue_post_params
      params.require(:queue_post).permit(:status_id, :acc_setting_id, :pool_post_id, :type, :title, :content, :extra_content, :tags, :image_file, :link, :other_field, :schedule_time)
    end
end
