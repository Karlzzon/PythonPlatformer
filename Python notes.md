
In python a function is defined with the keyword def followed by
the function name and a colon. The function body is indented with 4 spaces.
def function_name():
    function body

Arguments can be passed into a function by putting them in the parentheses.
    def addNum(num1, num2):
        print(num1 + num2)
    
    addNum(2, 4)
#outputs : 6

The return keyword can be used to return a value from a function.
    def addNum(num1, num2):
        return num1 + num2
    
    print(addNum(2, 4))
#outputs : 6


Python treats the statements with the same indentation level 
(statements with an equal number whitespaces before them) as a block of code.

For loops - For loops execute a block of code a fixed number of times.
You can iterate over a range, string, sequence, etc.
To count to 10 you can use the range function: 
    for i in range(1,11):
        print(i)	
The first number is inclusive and the second number is exclusive.
#outputs : 1 2 3 4 5 6 7 8 9 10

You can also use a for loop to iterate over a String.
Say you have the string credit_card = "1234-5678-9012-3456"
    for i in credit_card:
        print(i)
#outputs : 1 2 3 4 - 5 6 7 8 - 9 0 1 2 - 3 4 5 6


While loops - While loops execute a block of code as long as a condition is true.
    i = 1
    while i <= 10:
        print(i)
        i += 1
#outputs : 1 2 3 4 5 6 7 8 9 10

If statements - If statements are used to test for a condition and execute a block of code if the condition is true.
    if 1 < 2:
        print('1 is less than 2')
#outputs : 1 is less than 2


Underscores have a meaning in python variable and method names.
Some of that meaning is merely by convention and intended as a hint to the programmer and som of it is enforced by the python interpreter.


Single leading underscores : _var
    By convention, a single leading underscore indicates that the variable is for internal use only.
    This isnt enforced by Pthon, but it is a convention among Python programmers.

    However, leading underscores do impact how names get imported from modules. Imagine you had the following code in a module called 
    my_module :
        #this is my_module.py
        def external_func():
            return 23
        
        def _internal_func():
            return 42

Now if you use a wildcard import to import all names from the module,
python will NOT import names with a leading underscore.


Single trailing underscore : var_
Sometimes the most fitting name for a variable is already taken by a keyword in Python. Therefore names like class or def cant be used as variable names in Python. In this case you can append a single 
underscore to break the naming conflict.


Double leading underscore : __var
A double underscore prefix causes the Python interpreter to rewrite the attribute name in order to avoid naming conflicts in subclasses.
This is called name mangling- the interpreter changes the name of the
variable in a way that makes it harder to create collisions when the class is extended later.

Double leading and trailing underscores : __var__
This is the so-called magic method in Python. They are also known as dunder methods.
Here name mangling is not applied if a name starts and ends with double underscores. Variables surrounded by a double underscore prefix and suffix are left unscathed by the Python interpreter.

Single underscore : _
 Per convention a single standalone underscore is sometimes used as a name to indicate that a variable is temporary or insignificant.
 You can also use single underscore in unpacking expressions as a
 "dont care" variable to ignore particular values. 
 Again, this meaning is merely a convention and not enforced by Python.
 