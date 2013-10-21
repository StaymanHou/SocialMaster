class CreatePoolPostTypes < ActiveRecord::Migration
  def change
    create_table :pool_post_types do |t|
      t.string :title

      t.timestamps
    end
  end
end
