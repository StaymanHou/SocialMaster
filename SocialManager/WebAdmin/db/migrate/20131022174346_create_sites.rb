class CreateSites < ActiveRecord::Migration
  def change
    create_table :sites do |t|
      t.references :site_category, index: true
      t.string :domain

      t.timestamps
    end
  end
end
