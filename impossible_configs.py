# Dirty script to examine impossible shapes

from shapesearch import Shape

with open('shapes.log') as h:
	buildable_shapes = h.readlines()
	buildable_shapes = [ line[:-1].replace(':', '') for line in buildable_shapes ]

buildable_shapes.sort()

def get_all_shapes(n):
	if n == 0:
		return [ '' ]
	rest = get_all_shapes(n - 1)
	shapes = [ '#' + shape for shape in rest ]
	shapes.extend([ '.' + shape for shape in rest ])
	return shapes

all_shapes = get_all_shapes(16)

impossible = []
rest = buildable_shapes[:]
n = 0
while len(rest) > 0:
	try_shape = all_shapes.pop(0)
	if rest[0] == try_shape:
		_ = rest.pop(0)
	else:
		impossible.append(try_shape)

short_keys = [
	':'.join( shape[i:i+4] for i in range(0, 16, 4) )
	for shape in impossible
]

impossible_shapes = [ Shape(k) for k in short_keys ]

# No floating layers
impossible_shapes = [
	shape for shape in impossible_shapes if not (
	(not any(shape.layers[1]) and (any(shape.layers[2]) or any(shape.layers[3])))
	or (not any(shape.layers[2]) and any(shape.layers[3])
	))
]

layers_2 = [ s for s in impossible_shapes if not any(s.layers[3]) and not any(s.layers[2]) ]

layers_3 = [ s for s in impossible_shapes if not any(s.layers[3]) and any(s.layers[2]) ]

layers_4 = [ s for s in impossible_shapes if any(s.layers[3]) ]

def contains_layers(shape, layers):
	n = len(layers)
	for bottom in range(0, 4 - n + 1):
		if shape.layers[bottom:bottom + n] == layers:
			return True
	return False

irreducible_3 = []
for shape in layers_3:
	if not any( contains_layers(shape, small_shape.layers[0:2]) for small_shape in layers_2 ):
		print('Found 3 with no irreducible 2')
		irreducible_3.append(shape)

irreducible_4 = []
for shape in layers_4:
	if (
		not any( contains_layers(shape, small_shape.layers[0:3]) for small_shape in irreducible_3 )
		and not any( contains_layers(shape, small_shape.layers[0:2]) for small_shape in layers_2 )
	):
		print('Found 4 with no irreducible 2 or 3')
		irreducible_4.append(shape)

# Check: no buildable shape can contain an impossible shape
for key in buildable_shapes:
	shape = Shape(key)
	if any( contains_layers(shape, small_shape.layers[0:2]) for small_shape in layers_2 ):
		print('Found 2-layer counterexample')
		print(shape)
	# if any( contains_layers(shape, small_shape.layers[0:3]) for small_shape in layers_3 ):
	# 	print('Found 3-layer counterexample')
	# 	print(shape)
	# if any( contains_layers(shape, small_shape.layers[0:4]) for small_shape in layers_4 ):
	# 	print('Found 4-layer counterexample')
	# 	print(shape)

# Rotation/symmetry invariance

def get_all_orientations(shape):
	all_orientations = []
	for _ in range(0, 4):
		key = shape.rotate()
		all_orientations.append(key)
		shape = Shape(key)
	shape = Shape(shape.flip())
	for _ in range(0, 4):
		key = shape.rotate()
		all_orientations.append(key)
		shape = Shape(key)
	return all_orientations

def unique_orientation(shapes):
	by_kind = []
	for orig_shape in shapes:
		key = repr(orig_shape)
		all_orientations = get_all_orientations(orig_shape)
		found = False
		for group in by_kind:
			if group[0] in all_orientations:
				group.append(key)
				found = True
		if not found:
			by_kind.append([key])
	
	unique = []
	for group in by_kind:
		group.sort()
		unique.append(group[-1])
	unique.sort()
	return unique

unique_2 = [ Shape(key) for key in unique_orientation(layers_2) ]
unique_3 = [ Shape(key) for key in unique_orientation(irreducible_3) ]

# Sanity check
def check_unifier(full_shapes, unique_shapes):
	full_keys = [ repr(shape) for shape in full_shapes ]
	
	all_orientations = []
	for base_shape in unique_shapes:
		all_orientations.extend(get_all_orientations(base_shape))
	
	for key in all_orientations:
		if key not in full_keys:
			print('Shape was not in original list!')
			print(Shape(key))
	
	for key in full_keys:
		if key not in all_orientations:
			print('Shape not a rotation of unified list!')
			print(Shape(key))

check_unifier(layers_2, unique_2)
check_unifier(irreducible_3, unique_3)

for shape in unique_2:
	print(shape)

for shape in unique_3:
	print(shape)
