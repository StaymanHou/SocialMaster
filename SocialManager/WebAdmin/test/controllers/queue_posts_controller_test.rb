require 'test_helper'

class QueuePostsControllerTest < ActionController::TestCase
  setup do
    @queue_post = queue_posts(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:queue_posts)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create queue_post" do
    assert_difference('QueuePost.count') do
      post :create, queue_post: { acc_setting_id: @queue_post.acc_setting_id, content: @queue_post.content, extra_content: @queue_post.extra_content, image_file: @queue_post.image_file, link: @queue_post.link, other_field: @queue_post.other_field, rss_post_id: @queue_post.rss_post_id, schedule_time: @queue_post.schedule_time, status_id: @queue_post.status_id, tags: @queue_post.tags, title: @queue_post.title, type: @queue_post.type }
    end

    assert_redirected_to queue_post_path(assigns(:queue_post))
  end

  test "should show queue_post" do
    get :show, id: @queue_post
    assert_response :success
  end

  test "should get edit" do
    get :edit, id: @queue_post
    assert_response :success
  end

  test "should update queue_post" do
    patch :update, id: @queue_post, queue_post: { acc_setting_id: @queue_post.acc_setting_id, content: @queue_post.content, extra_content: @queue_post.extra_content, image_file: @queue_post.image_file, link: @queue_post.link, other_field: @queue_post.other_field, rss_post_id: @queue_post.rss_post_id, schedule_time: @queue_post.schedule_time, status_id: @queue_post.status_id, tags: @queue_post.tags, title: @queue_post.title, type: @queue_post.type }
    assert_redirected_to queue_post_path(assigns(:queue_post))
  end

  test "should destroy queue_post" do
    assert_difference('QueuePost.count', -1) do
      delete :destroy, id: @queue_post
    end

    assert_redirected_to queue_posts_path
  end
end
