require 'test_helper'

class PostDataControllerTest < ActionController::TestCase
  setup do
    @post_datum = post_data(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:post_data)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create post_datum" do
    assert_difference('PostDatum.count') do
      post :create, post_datum: { content: @post_datum.content, data: @post_datum.data, extra_content: @post_datum.extra_content, image_file: @post_datum.image_file, link: @post_datum.link, other_field: @post_datum.other_field, tags: @post_datum.tags, title: @post_datum.title, type: @post_datum.type }
    end

    assert_redirected_to post_datum_path(assigns(:post_datum))
  end

  test "should show post_datum" do
    get :show, id: @post_datum
    assert_response :success
  end

  test "should get edit" do
    get :edit, id: @post_datum
    assert_response :success
  end

  test "should update post_datum" do
    patch :update, id: @post_datum, post_datum: { content: @post_datum.content, data: @post_datum.data, extra_content: @post_datum.extra_content, image_file: @post_datum.image_file, link: @post_datum.link, other_field: @post_datum.other_field, tags: @post_datum.tags, title: @post_datum.title, type: @post_datum.type }
    assert_redirected_to post_datum_path(assigns(:post_datum))
  end

  test "should destroy post_datum" do
    assert_difference('PostDatum.count', -1) do
      delete :destroy, id: @post_datum
    end

    assert_redirected_to post_data_path
  end
end
