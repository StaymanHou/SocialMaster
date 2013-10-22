class CreateSiteCategories < ActiveRecord::Migration
  def change
    create_table :site_categories do |t|
      t.string :name

      t.timestamps
    end
  end
end
