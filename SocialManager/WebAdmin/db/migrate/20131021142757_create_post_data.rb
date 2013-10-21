class CreatePostData < ActiveRecord::Migration
  def change
    create_table :post_data do |t|
      t.integer :type
      t.string :title
      t.text :content
      t.string :extra_content
      t.string :tags
      t.string :image_file
      t.string :link
      t.string :other_field
      t.text :data

      t.timestamps
    end
  end
end
