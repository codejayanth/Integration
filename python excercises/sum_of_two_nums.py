def sum_of_two_nums(*args):
    '''
    The Function sum_of_two_nums can take any number of arguments and calculates the sum of it.
    The parameters can be any either negative or positive.
    '''
    sum = 0
    for arg in args:
        sum = sum + arg
    
    return sum

# Calling the Function
sum_of_one_to_ten = sum_of_two_nums(1,2,3,4,5,6,7,8,9,10)

print(sum_of_one_to_ten)