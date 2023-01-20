"""
Make a coordinate table for a matrix
"""
def generate_coordinate_table(width, height, serpentine=False):
    table = {}

    for y in range(0, height):
        for x in range(0, width):
            if not serpentine or (y % 2 == 0):
                # normal orientation row
                # all rows of non-serpentine matrices are like this
                # every other row of serpentine matrices are like this
                table[(x,y)] = (y * width) + x
            else:
                # flipped orientation row
                # every other row of serpentine matrices is like this
                table[(x,y)] = (y * width) + (width - x - 1)

    return table
