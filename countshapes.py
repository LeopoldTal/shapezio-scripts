def choose(n, k):
	"""
	A fast way to calculate binomial coefficients by Andrew Dalke
	"""
	if 0 <= k <= n:
		ntok = 1
		ktok = 1
		for t in range(1, min(k, n - k) + 1):
			ntok *= n
			ktok *= t
			n -= 1
		return ntok // ktok
	else:
		return 0

with open('shapes.log') as h:
	lines = h.readlines()

buildable_configurations_by_size = dict()
for n in range(0, 17):
	buildable_configurations_by_size[n] = 0
for line in lines:
	n = line.count('#')
	buildable_configurations_by_size[n] += 1

def pc(part, total):
	return '%.8f%%' % (part / total * 100,)

print('Filled-in quadrants\tAll configurations\tBuildable configurations\t%% buildable configs\tAll shapes\tBuildable shapes\t%% buildable shapes')
total_configurations = 0
total_buildable_configurations = 0
total_shapes = 0
total_buildable_shapes = 0
for n in range(0, 17):
	configurations = choose(16, n)
	buildable_configurations = buildable_configurations_by_size[n]
	
	shapes_per_configuration = 32**n
	shapes = shapes_per_configuration * configurations
	buildable_shapes = shapes_per_configuration * buildable_configurations
	
	total_configurations += configurations
	total_buildable_configurations += buildable_configurations
	total_shapes += shapes
	total_buildable_shapes += buildable_shapes
	
	print('%d\t%d\t%d\t%s\t%d\t%d\t%s' % (
		n,
		configurations, buildable_configurations, pc(buildable_configurations, configurations),
		shapes, buildable_shapes, pc(buildable_shapes, shapes)
	))

print('Total\t%d\t%d\t%s\t%d\t%d\t%s' % (
	total_configurations, total_buildable_configurations, pc(total_buildable_configurations, total_configurations),
	total_shapes, total_buildable_shapes, pc(total_buildable_shapes, total_shapes)
))
