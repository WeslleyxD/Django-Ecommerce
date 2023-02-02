class MyClass:
    def __init__(self, *args, **kwargs):
        # Recebe argumentos adicionais através de *args
        for arg in args:
            print(arg)

        # Recebe argumentos adicionais através de **kwargs
        for key, value in kwargs.items():
            print(f"{key}: {value}")

# Chame a classe e passe argumentos adicionais
my_obj = MyClass("arg1", "arg2", key1="value1", key2="value2")