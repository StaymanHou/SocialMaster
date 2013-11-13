class AddImageLinkToQueuePosts < ActiveRecord::Migration
  def change
    add_column :queue_posts, :image_link, :string
  end
end
