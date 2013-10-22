require 'test_helper'

class AccSettingsControllerTest < ActionController::TestCase
  setup do
    @acc_setting = acc_settings(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:acc_settings)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create acc_setting" do
    assert_difference('AccSetting.count') do
      post :create, acc_setting: { account_id: @acc_setting.account_id, active: @acc_setting.active, auto_mode_id: @acc_setting.auto_mode_id, extra_content: @acc_setting.extra_content, min_post_interval: @acc_setting.min_post_interval, num_per_day: @acc_setting.num_per_day, other_setting: @acc_setting.other_setting, password: @acc_setting.password, queue_size: @acc_setting.queue_size, smodule_id: @acc_setting.smodule_id, time_end: @acc_setting.time_end, time_start: @acc_setting.time_start, username: @acc_setting.username }
    end

    assert_redirected_to acc_setting_path(assigns(:acc_setting))
  end

  test "should show acc_setting" do
    get :show, id: @acc_setting
    assert_response :success
  end

  test "should get edit" do
    get :edit, id: @acc_setting
    assert_response :success
  end

  test "should update acc_setting" do
    patch :update, id: @acc_setting, acc_setting: { account_id: @acc_setting.account_id, active: @acc_setting.active, auto_mode_id: @acc_setting.auto_mode_id, extra_content: @acc_setting.extra_content, min_post_interval: @acc_setting.min_post_interval, num_per_day: @acc_setting.num_per_day, other_setting: @acc_setting.other_setting, password: @acc_setting.password, queue_size: @acc_setting.queue_size, smodule_id: @acc_setting.smodule_id, time_end: @acc_setting.time_end, time_start: @acc_setting.time_start, username: @acc_setting.username }
    assert_redirected_to acc_setting_path(assigns(:acc_setting))
  end

  test "should destroy acc_setting" do
    assert_difference('AccSetting.count', -1) do
      delete :destroy, id: @acc_setting
    end

    assert_redirected_to acc_settings_path
  end
end
