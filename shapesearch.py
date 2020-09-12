"""Compute all buildable configurations"""

def to_short_key(layers):
	return ':'.join(
			''.join('#' if quad else '.' for quad in layer)
			for layer in layers
		)

class Shape: # A configuration of quadrants without shape-type / colour info
	def __init__(self, short_key):
		self.layers = [
			[ quad == '#' for quad in layer ]
			for layer in short_key.split(':')
		]
	
	def __repr__(self):
		return to_short_key(self.layers)
	
	def __str__(self):
		show_quad = lambda quad: '#' if quad else '.'
		lineTop = '  '.join(
			show_quad(layer[3]) + show_quad(layer[0])
			for layer in self.layers
		) + '\n'
		lineBottom = '  '.join(
			show_quad(layer[2]) + show_quad(layer[1])
			for layer in self.layers
		) + '\n'
		return '\n' + lineTop + lineBottom
	
	# Transforms
	def cut(self): # vertical cut only
		def cut_layer(layer):
			return (
				(layer[0], layer[1], False, False),
				(False, False, layer[2], layer[3])
			)
		def drop(layers):
			floor_layers = []
			for layer in layers:
				if any(quad for quad in layer):
					floor_layers.append(layer)
			while len(floor_layers) < 4:
				floor_layers.append( (False, False, False, False) )
			return floor_layers
		right, left = zip(*[ cut_layer(layer) for layer in self.layers ])
		right, left = drop(right), drop(left)
		return (to_short_key(left), to_short_key(right))
	
	def rotate(self): # clockwise quarter rotation only
		def rotate_layer(layer):
			return (layer[3], layer[0], layer[1], layer[2])
		new_layers = [rotate_layer(layer) for layer in self.layers]
		return to_short_key(new_layers)
	
	def stack(self, top_shape):
		if not any(quad for quad in top_shape.layers[0]):
			raise ValueError(
				'Entirely floating shape - this should never happen! ' + repr(top_shape)
			)
		
		def can_merge_into(merging_at):
			for layer_num in range(merging_at, 4):
				into_layer = self.layers[layer_num]
				falling_layer = top_shape.layers[layer_num - merging_at]
				if any(into_layer[quad] and falling_layer[quad] for quad in range(4)):
					return False
			return True
		
		def merge_layers(into_layer, falling_layer):
			return ( into_layer[quad] or falling_layer[quad] for quad in range(4) )
		
		merging_at = 4
		while merging_at > 0 and can_merge_into(merging_at - 1):
			merging_at -= 1
		
		new_layers = []
		for layer_num in range(merging_at):
			new_layers.append(self.layers[layer_num])
		
		for layer_num in range(merging_at, 4):
			into_layer = self.layers[layer_num]
			falling_layer = top_shape.layers[layer_num - merging_at]
			new_layers.append(merge_layers(into_layer, falling_layer))
		
		return to_short_key(new_layers)
	
	def flip(self): # not an in-game operation, used to compute unique impossible shapes
		def flip_layer(layer):
			return (layer[0], layer[3], layer[2], layer[1])
		new_layers = [flip_layer(layer) for layer in self.layers]
		return to_short_key(new_layers)

def search_all_shapes():
	with open('shapes.log', 'w') as log:
		closed = set()
		to_search = set()
		n = 0
		
		def add(shape):
			if shape != '....:....:....:....': # the empty shape is not a shape
				if shape not in closed:
					to_search.add(shape)
		
		start_shape = '####:....:....:....'
		add(start_shape)
		
		while to_search:
			new_key = to_search.pop()
			closed.add(new_key)
			
			shape = Shape(new_key)
			log.write(new_key + '\n')
			
			n += 1
			if n % 1000 == 0:
				print(n)
				print(shape)
			
			add(shape.rotate())
			
			left, right = shape.cut()
			add(left)
			add(right)
			
			for old_key in closed:
				old_shape = Shape(old_key)
				add(old_shape.stack(shape))
				add(shape.stack(old_shape))
	
	print('Generated', len(closed), 'shapes.')

if __name__ == '__main__':
	search_all_shapes()
