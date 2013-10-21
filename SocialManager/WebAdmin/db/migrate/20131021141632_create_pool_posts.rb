class CreatePoolPosts < ActiveRecord::Migration
  def change
    create_table :pool_posts do |t|
      t.boolean :hidden
      t.string :title
      t.string :description
      t.text :content
      t.string :tags
      t.string :image_file
      t.string :image_link
      t.string :link
      t.integer :social_score

      t.timestamps
    end
  end
end
