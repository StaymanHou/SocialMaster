# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20131022175757) do

  create_table "acc_settings", force: true do |t|
    t.integer  "account_id"
    t.integer  "smodule_id"
    t.string   "username"
    t.string   "password"
    t.string   "other_setting"
    t.string   "extra_content"
    t.boolean  "active"
    t.integer  "auto_mode_id"
    t.time     "time_start"
    t.time     "time_end"
    t.integer  "num_per_day"
    t.integer  "min_post_interval"
    t.integer  "queue_size"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  add_index "acc_settings", ["account_id"], name: "index_acc_settings_on_account_id", using: :btree
  add_index "acc_settings", ["auto_mode_id"], name: "index_acc_settings_on_auto_mode_id", using: :btree
  add_index "acc_settings", ["smodule_id"], name: "index_acc_settings_on_smodule_id", using: :btree

  create_table "accounts", force: true do |t|
    t.string   "name"
    t.string   "rss_urls"
    t.boolean  "active"
    t.datetime "last_update"
    t.boolean  "deleted"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "auto_modes", force: true do |t|
    t.string   "title"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "pool_post_types", force: true do |t|
    t.string   "title"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "pool_posts", force: true do |t|
    t.integer  "account_id"
    t.integer  "pool_post_type_id"
    t.integer  "site_id"
    t.boolean  "hidden"
    t.string   "title"
    t.string   "description"
    t.text     "content"
    t.string   "tags"
    t.string   "image_file"
    t.string   "image_link"
    t.string   "link"
    t.integer  "social_score"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  add_index "pool_posts", ["account_id"], name: "index_pool_posts_on_account_id", using: :btree
  add_index "pool_posts", ["pool_post_type_id"], name: "index_pool_posts_on_pool_post_type_id", using: :btree
  add_index "pool_posts", ["site_id"], name: "index_pool_posts_on_site_id", using: :btree

  create_table "post_data", force: true do |t|
    t.integer  "acc_setting_id"
    t.integer  "type"
    t.string   "title"
    t.text     "content"
    t.string   "extra_content"
    t.string   "tags"
    t.string   "image_file"
    t.string   "link"
    t.string   "other_field"
    t.text     "data"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  add_index "post_data", ["acc_setting_id"], name: "index_post_data_on_acc_setting_id", using: :btree

  create_table "queue_posts", force: true do |t|
    t.integer  "status_id"
    t.integer  "acc_setting_id"
    t.integer  "pool_post_id"
    t.integer  "type"
    t.string   "title"
    t.text     "content"
    t.string   "extra_content"
    t.string   "tags"
    t.string   "image_file"
    t.string   "link"
    t.string   "other_field"
    t.datetime "schedule_time"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  add_index "queue_posts", ["acc_setting_id"], name: "index_queue_posts_on_acc_setting_id", using: :btree
  add_index "queue_posts", ["pool_post_id"], name: "index_queue_posts_on_pool_post_id", using: :btree
  add_index "queue_posts", ["status_id"], name: "index_queue_posts_on_status_id", using: :btree

  create_table "site_categories", force: true do |t|
    t.string   "name"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "sites", force: true do |t|
    t.integer  "site_category_id"
    t.string   "domain"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  add_index "sites", ["site_category_id"], name: "index_sites_on_site_category_id", using: :btree

  create_table "smodules", force: true do |t|
    t.string   "name"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "statuses", force: true do |t|
    t.string   "title"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "tags", force: true do |t|
    t.integer  "site_id"
    t.string   "str"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  add_index "tags", ["site_id"], name: "index_tags_on_site_id", using: :btree

end
