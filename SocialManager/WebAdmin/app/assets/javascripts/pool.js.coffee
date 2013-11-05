# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

account = $('#rss-table').data('account')

PoolPostItem = Backbone.Model.extend
	urlRoot: "/pool_posts"

PoolPostView = Backbone.View.extend
	tagName: 'tr'
	template: _.template('<td><%= title %></td><td>something</td>
	<td>something</td>
	<td>something</td>
	<td>something</td>
	<td>something</td>')
	render: ->
		@.$el.html(@.template(@.model.toJSON()))

PoolPostList = Backbone.Collection.extend
	model: PoolPostItem
	url: '/pool_posts.json'

PoolPostListView = Backbone.View.extend
	preventLoad: false
	events: 
		'scroll': 'scroll'
	tagName: 'tbody'
	initialize: ->
		@.collection.on('reset', @addAll, @)
	render: ->
		@.addAll()
	scroll: ->
		if not @.preventLoad and @.$el.children().last().offset().top - @.$el.children().last().height() <= @.$el.height()
			@.preventLoad = true
			@.collection.fetch({reset: true})
	addAll: ->
		@.collection.forEach(@.addOne, @)
		@.preventLoad = false
	addOne: (poolpostItem) ->
		poolpostView = new PoolPostView
			model: poolpostItem
		poolpostView.render()
		@.$el.append(poolpostView.el)

poolpostList = new PoolPostList()
poolpostListView = new PoolPostListView
	collection: poolpostList

poolpostList.fetch({reset: true})

$('#rss-table').append(poolpostListView.el)
