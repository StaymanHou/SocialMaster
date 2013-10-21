require 'test_helper'

class AutoModesControllerTest < ActionController::TestCase
  setup do
    @auto_mode = auto_modes(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:auto_modes)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create auto_mode" do
    assert_difference('AutoMode.count') do
      post :create, auto_mode: { title: @auto_mode.title }
    end

    assert_redirected_to auto_mode_path(assigns(:auto_mode))
  end

  test "should show auto_mode" do
    get :show, id: @auto_mode
    assert_response :success
  end

  test "should get edit" do
    get :edit, id: @auto_mode
    assert_response :success
  end

  test "should update auto_mode" do
    patch :update, id: @auto_mode, auto_mode: { title: @auto_mode.title }
    assert_redirected_to auto_mode_path(assigns(:auto_mode))
  end

  test "should destroy auto_mode" do
    assert_difference('AutoMode.count', -1) do
      delete :destroy, id: @auto_mode
    end

    assert_redirected_to auto_modes_path
  end
end
