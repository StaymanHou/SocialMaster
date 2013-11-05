# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

if $('#rss-table').length

	account_id = $('#rss-table').data('account')
	cursor = $('#rss-table').data('cursor')

	PoolPostItem = Backbone.Model.extend
		urlRoot: "/pool_posts"
		hide: ->
			@.set
				'hidden': true
			@.save()

	PoolPostView = Backbone.View.extend
		events:
			'click div.pool-post': 'modal'
			'click a.hide-trigger': 'hide'
		modal: ->
			$('#myModal').modal()
		hide: ->
			@.model.hide()
			@.$el.remove()
			false
		tagName: 'tr'
		template: _.template('
			<td><div class="pool-post">
				<p><%= title %></p>
				<div><img src="../images/postimg/rss/<%= image_file %>"></img></div>
				<p><%= created_at.substring(0,19).replace("T"," ") %></p>
				<p></p>
			</div><a href="#" class="btn btn-mini hide-trigger">Hide</a></td>
			<td>something</td>
			<td>something</td>
			<td>something</td>
			<td>something</td>
			<td>something</td>
		')
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
				@.collection.fetch
					reset: true
					data: $.param({ account_id: account_id, hidden: false, cursor: cursor})
		addAll: ->
			@.collection.forEach(@.addOne, @)
			cursor += @.collection.length
			if @.collection.length == 30
				@.preventLoad = false
		addOne: (poolpostItem) ->
			poolpostView = new PoolPostView
				model: poolpostItem
			poolpostView.render()
			@.$el.append(poolpostView.el)

	poolpostList = new PoolPostList()
	poolpostListView = new PoolPostListView
		collection: poolpostList

	poolpostList.fetch
		reset: true
		data: $.param({ account_id: account_id, hidden: false, cursor: cursor})

	$('#rss-table').append(poolpostListView.el)

