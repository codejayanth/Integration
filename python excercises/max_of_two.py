# The maximum of two numbers, we will use the conditional if-else statements for this

def max_of_two_nums(a,b):
    '''
    The function max_of_two_nums will take two parameters and returns a string stating either greater or equal or lesser.
    '''
    if a > b:
        return f"Value a is greater than value b"
    elif a == b:
        return f"Value a is equal to value b"
    else:
        return f"Value a is less than value b"
    

print(max_of_two_nums(45, 78))