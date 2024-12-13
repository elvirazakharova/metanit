from django.test import TestCase

# Create your tests here.
def sum(*numbers):
    result = 0
    for n in numbers:
        result += n
    print(f"sum = {result}")

def far(*arg1):
    result = 0
    for i in arg1:
        result += i
 
 
sum(1, 2, 3, 4, 5)      # sum = 15
sum(3, 4, 5, 6)         # sum = 18



a = far(11, 12, 13) 
print(f"far(11, 12, 13) = {a}")  