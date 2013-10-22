require 'test_helper'

class PoolPostsControllerTest < ActionController::TestCase
  setup do
    @pool_post = pool_posts(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:pool_posts)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create pool_post" do
    assert_difference('PoolPost.count') do
      post :create, pool_post: { account_id: @pool_post.account_id, content: @pool_post.content, description: @pool_post.description, hidden: @pool_post.hidden, image_file: @pool_post.image_file, image_link: @pool_post.image_link, link: @pool_post.link, pool_post_type_id: @pool_post.pool_post_type_id, site_id: @pool_post.site_id, social_score: @pool_post.social_score, tags: @pool_post.tags, title: @pool_post.title }
    end

    assert_redirected_to pool_post_path(assigns(:pool_post))
  end

  test "should show pool_post" do
    get :show, id: @pool_post
    assert_response :success
  end

  test "should get edit" do
    get :edit, id: @pool_post
    assert_response :success
  end

  test "should update pool_post" do
    patch :update, id: @pool_post, pool_post: { account_id: @pool_post.account_id, content: @pool_post.content, description: @pool_post.description, hidden: @pool_post.hidden, image_file: @pool_post.image_file, image_link: @pool_post.image_link, link: @pool_post.link, pool_post_type_id: @pool_post.pool_post_type_id, site_id: @pool_post.site_id, social_score: @pool_post.social_score, tags: @pool_post.tags, title: @pool_post.title }
    assert_redirected_to pool_post_path(assigns(:pool_post))
  end

  test "should destroy pool_post" do
    assert_difference('PoolPost.count', -1) do
      delete :destroy, id: @pool_post
    end

    assert_redirected_to pool_posts_path
  end
end
