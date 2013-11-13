class RenameQueuePostTypeToPostType < ActiveRecord::Migration
  def change
  	rename_column :queue_posts, :type, :post_type
  end
end
