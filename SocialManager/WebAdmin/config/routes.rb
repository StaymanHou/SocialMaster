WebAdmin::Application.routes.draw do
  # The priority is based upon order of creation: first created -> highest priority.
  # See how all your routes lay out with "rake routes".

  # You can have the root of your site routed with "root"
  root 'home#index'

  # Example of regular route:
  #   get 'products/:id' => 'catalog#view'
  get "pool/rss", as: :pool_rss
  get "pool/web", as: :pool_web
  get "pool/social", as: :pool_social
  get "queue/index", as: :queue_index
  get "performance/index", as: :performance_index
  get "home/index"
  get 'accounts/:id/toggle_active' => 'accounts#toggle_active', as: :account_toggle_active
  get 'acc_settings/:id/toggle_active' => 'acc_settings#toggle_active', as: :acc_setting_toggle_active

  # Example of named route that can be invoked with purchase_url(id: product.id)
  #   get 'products/:id/purchase' => 'catalog#purchase', as: :purchase
  get 'pool_posts/new/:from/:pool_post_type_id/:account_id' => 'pool_posts#new', as: :new_pool_post

  # Example resource route (maps HTTP verbs to controller actions automatically):

  # Example resource route with options:
  #   resources :products do
  #     member do
  #       get 'short'
  #       post 'toggle'
  #     end
  #
  #     collection do
  #       get 'sold'
  #     end
  #   end

  # Example resource route with sub-resources:
  #   resources :products do
  #     resources :comments, :sales
  #     resource :seller
  #   end

  resources :post_data

  resources :auto_modes

  resources :smodules

  resources :acc_settings

  resources :accounts

  resources :statuses

  resources :queue_posts

  resources :pool_post_types

  resources :pool_posts

  resources :site_categories

  resources :sites do
    resources :tags
  end

  resources :tags

  # Example resource route with more complex sub-resources:
  #   resources :products do
  #     resources :comments
  #     resources :sales do
  #       get 'recent', on: :collection
  #     end
  #   end
  
  # Example resource route with concerns:
  #   concern :toggleable do
  #     post 'toggle'
  #   end
  #   resources :posts, concerns: :toggleable
  #   resources :photos, concerns: :toggleable

  # Example resource route within a namespace:
  #   namespace :admin do
  #     # Directs /admin/products/* to Admin::ProductsController
  #     # (app/controllers/admin/products_controller.rb)
  #     resources :products
  #   end
end
