def make_greeter(greeting):
    def greet(name):
        print(f"{greeting}, {name}!")
    return greet

hello_greeter = make_greeter("Hello")   # Step 1
#hello_greeter("Abi")      
print(hello_greeter.__name__)               # Step 2 → prints "Hello, Abi!"