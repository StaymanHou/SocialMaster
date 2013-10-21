class CreateAutoModes < ActiveRecord::Migration
  def change
    create_table :auto_modes do |t|
      t.string :title

      t.timestamps
    end
  end
end
