class AddTagLimitToAccounts < ActiveRecord::Migration
  def change
    add_column :accounts, :tag_limit, :integer
  end
end
