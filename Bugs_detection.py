import ast
import builtins
#1)if there is arithmatic operation in ensure that the arguments is numeric
def is_number(code):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod)):
                if (is_numeric_variable(code,node.left.id)) and (is_numeric_variable(code, node.right.id)):
                    return True 
                else:
                    return  False 
    return  "No arithmetic operation found"


def is_numeric_variable(code, var_name):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == var_name:
            if isinstance(node.value, ast.Num):
                return True
            else:
                return False
    return False
    
#2)if it is subjected to buffer overflow or not 
def buffer_overflow(code):
    # Check if the code contains a potential buffer overflow vulnerability
    if "[]" in code or "memset" in code:
        return True 
    else:
        esmha=''
        esmha2=''
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                if node.value.func.id == "input":
                    esmha = node.targets[0].id
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == "len" and  isinstance(node.args[0], ast.Name):
                    esmha2 = node.args[0].id
                    
                    if esmha == esmha2:
                        return False
                    else:
                        return True 
    return True 
#3)def test

def def_test(code):
    
    tree = ast.parse(code)
    defined_vars = set()
    used_vars = set()
    
    # Find all defined variables
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for var_name in node.targets:
                if isinstance(var_name, ast.Name):
                    defined_vars.add(var_name.id)
    #used
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Load):
                used_vars.add(node.id)
    
    
    for var in defined_vars:
        if var not in used_vars:
            return False, f" '{var}' is defined but not used"
    
    return True ,"All deined is used"

#4)indentation error
def has_indentation_error(code):
    # Check if the code contains indentation errors
    try:
        compiled_code = compile(code, "<string>", "exec")
        return False 
    except IndentationError as I:
        
        return f"Code has an indentation error at:{I.lineno}, column {I.offset}"
    
#5)infinite loop    
def has_infinite_loop(code):
    
    tree = ast.parse(code)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            if isinstance(node.test, ast.Constant) and node.test.value == True:
                return True 
            else:
                return False
        elif isinstance(node, ast.For):
            if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':
                start = 0
                step = 1
                if len(node.iter.args) == 1:
                    stop = node.iter.args[0]
                elif len(node.iter.args) == 2:
                    start = node.iter.args[0]
                    stop = node.iter.args[1]
                elif len(node.iter.args) == 3:#range(2,10,2)
                    start = node.iter.args[0]
                    stop = node.iter.args[1]
                    step = node.iter.args[2]
                
                if start < stop and step <= 0:
                    return True 
                elif start > stop and step >= 0:
                    return True 
    
    return False , "no infinite loop"
#6_input validatiom
def input_validation(code):
    # Check if the code contains input validation
    if "input" in code and "try" in code:
        return True 
    return False 
#7)syntax error
def syntaxerror(code):
    try:
        ast.parse(code)
        return "No syntax error found"
    except SyntaxError as s:
        return f"Syntax Error at line ({s.lineno}:{s.offset}) {s.msg}"

#8)usetest
def use_test(code):
    tree = ast.parse(code)
    definedV = set()
    usedV = set()
    constants = set()
    functions = set()
    
    # Define print as a built-in function
    builtins.print = print
    functions.add('print')
    functions.add('input')
    functions.add('int')
    functions.add('len')
    functions.add('ValueError')

    
    # Find all defined variables
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for var_name in node.targets:
                if isinstance(var_name, ast.Name):
                    definedV.add(var_name.id)
    
    # Find all used variables and functions
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Load):
                usedV.add(node.id)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name not in dir(builtins):
                    functions.add(func_name)
        elif isinstance(node, (ast.Num, ast.Str, ast.Bytes)):
            constants.add(node.n)
    
    # Check that every variable used is defined before use
    definedV.add('e')
    undefined_vars = usedV - definedV.union(functions)
    if undefined_vars:
        return f"Error: undefined variables used: {', '.join(undefined_vars)}"
    
    
    # All tests passed
    return "All variable usage tests passed"    

#runtine
def runtimeerror(code):
    try:
        exec(code)
    except Exception as e:
        return f"Runtime Error: {e}"
    else:
        return "Code executed successfully without any runtime errors"
    
code='''
while True:
    try:
        
        nterms = ["How many terms?"]
        while True:  # infinite loop
            if len(nterms) < 50:
                nterms = int(nterms)   
                n1 = 6
                n2 = 5
                
                
                if nterms <= 0:
                    print("Please enter a positive integer")
                    break  # exit inner loop
                
                elif nterms == 1:
                    print("Fibonacci sequence upto", nterms, ":")
                    
                    break  # exit inner loop
                
                else:
                    print("Fibonacci sequence:")
                    while count < nterms:
                        
                        nth = n1 + n2
                        # update values
                        n1 = n2
                        n2 = nth
                        count += 1
                    break  # exit inner loop
            
            else:
                print("too high")
                break  # exit inner loop
    
    except ValueError as e:
        print(e)
'''
code2="""
while True:
    try:
        
        nterms = ["How many terms?"]
        while True:  # infinite loop
            if len(nterms) < 50:
                nterms = int(nterms)   
                n1 = 0
                n2 = '1'
                
                
                if nterms <= 0:
                    print("Please enter a positive integer")
                    break  # exit inner loop
                
                elif nterms == 1:
                    print("Fibonacci sequence upto", nterms, ":")
                    
                    break  # exit inner loop
                
                else:
                    print("Fibonacci sequence:")
                    while count < nterms:
                        
                        nth = n2 + n2
                        # update values
                        n1 = n2
                        n2 = nth
                        count += 1
                    break  # exit inner loop
            
            else:
                print("too high")
                break  # exit inner loop
    
    except ValueError as e:
    print(e)"
"""


res1=is_number(code)
if res1:
    print("-Arithmetic operation with numeric arguments")
elif res1==False:
    print("-Arithmetic operation with non-numeric arguments")
else:
    print(res1)

res2=buffer_overflow(code)
if res2:
    print("-there is buffer overflow may happen")
else:
    print("-no buffer overflow ")

res3,m=def_test(code)
print("-",m)
res4=has_indentation_error(code2)
if res4:
    print("-",res4)
else:
    print("no identation error")

res5=has_infinite_loop(code)
if res5:
    print("-loop is infinite loop")
else:
    print(" has no infinite loop")

res6=input_validation(code)
if res6:
    print("there is input validation")
else:
    print("-No input validation")

res7=syntaxerror(code2)
print("-",res7)

res8=use_test(code)
print("-",res8)

res9=runtimeerror(code)
print("-",res9)
