require 'test_helper'

class SiteCategoriesControllerTest < ActionController::TestCase
  setup do
    @site_category = site_categories(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:site_categories)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create site_category" do
    assert_difference('SiteCategory.count') do
      post :create, site_category: { name: @site_category.name }
    end

    assert_redirected_to site_category_path(assigns(:site_category))
  end

  test "should show site_category" do
    get :show, id: @site_category
    assert_response :success
  end

  test "should get edit" do
    get :edit, id: @site_category
    assert_response :success
  end

  test "should update site_category" do
    patch :update, id: @site_category, site_category: { name: @site_category.name }
    assert_redirected_to site_category_path(assigns(:site_category))
  end

  test "should destroy site_category" do
    assert_difference('SiteCategory.count', -1) do
      delete :destroy, id: @site_category
    end

    assert_redirected_to site_categories_path
  end
end
