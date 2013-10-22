class CreateAccounts < ActiveRecord::Migration
  def change
    create_table :accounts do |t|
      t.string :name
      t.string :rss_urls
      t.boolean :active
      t.datetime :last_update
      t.boolean :deleted

      t.timestamps
    end
  end
end
