class CreateSmodules < ActiveRecord::Migration
  def change
    create_table :smodules do |t|
      t.string :name

      t.timestamps
    end
  end
end
