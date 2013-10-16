require 'test_helper'

class PoolControllerTest < ActionController::TestCase
  test "should get rss" do
    get :rss
    assert_response :success
  end

  test "should get web" do
    get :web
    assert_response :success
  end

  test "should get social" do
    get :social
    assert_response :success
  end

end
