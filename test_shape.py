import pytest
from shapesearch import Shape

class TestBuildShape:
	def test_repr(self):
		key = '##.#:..#.:....:....'
		shape = Shape(key)
		assert repr(shape) == key
	
	def test_str(self):
		key = '##.#:..#.:.##.:##..'
		pretty = str(Shape(key))
		assert pretty == """
##  ..  ..  .#
.#  #.  ##  .#
"""

class TestRotate:
	def test_spiral(self):
		shape = Shape('#...:.#..:..#.:...#')
		rotated = shape.rotate()
		assert rotated == '.#..:..#.:...#:#...'

class TestCut:
	def test_full_layer(self):
		shape = Shape('####:....:....:....')
		left, right = shape.cut()
		assert left == '..##:....:....:....'
		assert right == '##..:....:....:....'
	
	def test_vertical(self):
		shape = Shape('..##:....:....:....')
		left, right = shape.cut()
		assert left == '..##:....:....:....'
		assert right == '....:....:....:....'
	
	def test_horizontal(self):
		shape = Shape('#..#:....:....:....')
		left, right = shape.cut()
		assert left == '...#:....:....:....'
		assert right == '#...:....:....:....'
	
	def test_two_layers(self):
		shape = Shape('####:####:....:....')
		left, right = shape.cut()
		assert left == '..##:..##:....:....'
		assert right == '##..:##..:....:....'
	
	def test_drop(self):
		shape = Shape('#...:...#:....:....')
		left, right = shape.cut()
		assert left == '...#:....:....:....'
		assert right == '#...:....:....:....'
	
	def test_scaffolding_prevents_drop(self):
		shape = Shape('#.#.:...#:....:....')
		left, right = shape.cut()
		assert left == '..#.:...#:....:....'
		assert right == '#...:....:....:....'
	
	def test_long_drop(self):
		shape = Shape('#...:...#:.#..:..#.')
		left, right = shape.cut()
		assert left == '...#:..#.:....:....'
		assert right == '#...:.#..:....:....'

class TestStack:
	def test_no_empty_shape(self):
		empty = Shape('....:....:....:....')
		with pytest.raises(ValueError):
			empty.stack(empty)
	
	def test_simple_merge(self):
		bottom = Shape('##..:....:....:....')
		top = Shape('..##:....:....:....')
		merged = bottom.stack(top)
		assert merged == '####:....:....:....'
	
	def test_diagonal(self):
		bottom = Shape('...#:....:....:....')
		top = Shape('.#..:....:....:....')
		merged = bottom.stack(top)
		assert merged == '.#.#:....:....:....'
	
	def test_stack_full_layers(self):
		bottom = Shape('####:....:....:....')
		top = Shape('####:....:....:....')
		merged = bottom.stack(top)
		assert merged == '####:####:....:....'
	
	def test_stack_tall(self):
		bottom = Shape('#...:#...:....:....')
		top = Shape('#...:#...:....:....')
		merged = bottom.stack(top)
		assert merged == '#...:#...:#...:#...'
	
	def test_stack_angle(self):
		bottom = Shape('##..:....:....:....')
		top = Shape('.##.:....:....:....')
		merged = bottom.stack(top)
		assert merged == '##..:.##.:....:....'
	
	def test_stack_merge_on_second_layer(self):
		bottom = Shape('##..:#...:....:....')
		top = Shape('.##.:....:....:....')
		merged = bottom.stack(top)
		assert merged == '##..:###.:....:....'
	
	def test_staircase(self):
		bottom = Shape('#..#:##..:....:....')
		top = Shape('.##.:..##:....:....')
		merged = bottom.stack(top)
		assert merged == '#..#:##..:.##.:..##'
	
	def test_long_drop(self):
		bottom = Shape('#...:#...:#...:#...')
		top = Shape('.#..:....:....:....')
		merged = bottom.stack(top)
		assert merged == '##..:#...:#...:#...'
	
	def test_trim_to_four_layers(self):
		bottom = Shape('#...:#...:...#:....')
		top = Shape('####:...#:....:....')
		merged = bottom.stack(top)
		assert merged == '#...:#...:...#:####'
	
	def test_tetris(self):
		bottom = Shape('.##.:..#.:..#.:....')
		top = Shape('.#..:.##.:....:....')
		merged = bottom.stack(top)
		assert merged == '.##.:..#.:.##.:.##.'
	
	def test_logo(self):
		left_half = Shape('...#:..#.:....:....')
		right_half = Shape('##..:....:....:....')
		logo = left_half.stack(right_half)
		assert logo == '##.#:..#.:....:....'
