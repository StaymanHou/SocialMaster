require 'test_helper'

class SmodulesControllerTest < ActionController::TestCase
  setup do
    @smodule = smodules(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:smodules)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create smodule" do
    assert_difference('Smodule.count') do
      post :create, smodule: { name: @smodule.name }
    end

    assert_redirected_to smodule_path(assigns(:smodule))
  end

  test "should show smodule" do
    get :show, id: @smodule
    assert_response :success
  end

  test "should get edit" do
    get :edit, id: @smodule
    assert_response :success
  end

  test "should update smodule" do
    patch :update, id: @smodule, smodule: { name: @smodule.name }
    assert_redirected_to smodule_path(assigns(:smodule))
  end

  test "should destroy smodule" do
    assert_difference('Smodule.count', -1) do
      delete :destroy, id: @smodule
    end

    assert_redirected_to smodules_path
  end
end
