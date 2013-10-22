class CreateQueuePosts < ActiveRecord::Migration
  def change
    create_table :queue_posts do |t|
      t.references :status, index: true
      t.references :acc_setting, index: true
      t.references :rss_post, index: true
      t.integer :type
      t.string :title
      t.text :content
      t.string :extra_content
      t.string :tags
      t.string :image_file
      t.string :link
      t.string :other_field
      t.datetime :schedule_time

      t.timestamps
    end
  end
end
