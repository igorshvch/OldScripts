def matrix(rows, cols, iterable):
	if (rows*cols) != len(iterable):
		return 0
	else:
		matrix = [[[] for i in range(cols)] for j in range(rows)]
		for row in range(rows):
			for col in range(cols):
				matrix[row][col] = iterable.pop(0)
	return matrix
