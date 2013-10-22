class CreateAccSettings < ActiveRecord::Migration
  def change
    create_table :acc_settings do |t|
      t.references :account, index: true
      t.references :smodule, index: true
      t.string :username
      t.string :password
      t.string :other_setting
      t.string :extra_content
      t.boolean :active
      t.references :auto_mode, index: true
      t.time :time_start
      t.time :time_end
      t.integer :num_per_day
      t.integer :min_post_interval
      t.integer :queue_size

      t.timestamps
    end
  end
end
