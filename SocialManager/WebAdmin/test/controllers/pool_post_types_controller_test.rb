require 'test_helper'

class PoolPostTypesControllerTest < ActionController::TestCase
  setup do
    @pool_post_type = pool_post_types(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:pool_post_types)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create pool_post_type" do
    assert_difference('PoolPostType.count') do
      post :create, pool_post_type: { title: @pool_post_type.title }
    end

    assert_redirected_to pool_post_type_path(assigns(:pool_post_type))
  end

  test "should show pool_post_type" do
    get :show, id: @pool_post_type
    assert_response :success
  end

  test "should get edit" do
    get :edit, id: @pool_post_type
    assert_response :success
  end

  test "should update pool_post_type" do
    patch :update, id: @pool_post_type, pool_post_type: { title: @pool_post_type.title }
    assert_redirected_to pool_post_type_path(assigns(:pool_post_type))
  end

  test "should destroy pool_post_type" do
    assert_difference('PoolPostType.count', -1) do
      delete :destroy, id: @pool_post_type
    end

    assert_redirected_to pool_post_types_path
  end
end
