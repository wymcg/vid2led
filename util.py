"""
Make a coordinate table for a matrix
"""
def generate_coordinate_table(width, height, serpentine=False, vertical=False):
    table = {}

    if not vertical:
        # the matrix is wired horizontally (ie. every row is sequentially wired)
        for y in range(0, height):
            for x in range(0, width):
                if not serpentine or (y % 2 == 0):
                    # normal orientation row (horizontal)
                    # all rows of non-serpentine matrices are like this
                    # every other row of serpentine matrices are like this
                    table[(x, y)] = (y * width) + x
                else:
                    # flipped orientation row (horizontal)
                    # every other row of serpentine matrices is like this
                    table[(x, y)] = (y * width) + (width - x - 1)
    else:
        # the matrix is wired vertically (ie. each column is sequentially wired)
        for x in range(0, width):
            for y in range(0, height):
                if not serpentine or (x % 2 == 0):
                    # normal orientation column (vertical)
                    # all columns of non-serpentine matrices are like this
                    # every other column of serpentine matrices are like this
                    table[(x, y)] = (x * height) + y
                else:
                    # flipped orientation row (vertical)
                    # every other column of serpentine matrices are like this
                    table[(x, y)] = (x * height) + (height - y - 1)

    return table
