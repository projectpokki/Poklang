# Poklang (Prototype version)
Poklang is a lightweight, dynamic, imperative, unstructured programming language. It revolves around chaining "commands" (very basic functions/instructions) to manipulate variables. There are 31 commands in Poklang, allowing for basic math operations, string manipulation, console IO and boolean logic. variables can be nums (floats), strs or bools. I finished making this on February 2, 2024.

There is an interpreter for the prototpe version of Poklang in the ```Poklang prototype``` file. 4 python files, ```main.py```, ```LexerModule.py```, ```ParserModule.py``` and ```ExecutorModule.py```, work together to interpret Poklang code. ```PoklangInterpreter.py``` is all 4 python files joined together as one. The file that is run is ```Poklang.txt```. As per tradition, there is a script that prints "Hello, World!".

The language itself has many problems, like the lack of array manipulation, file IO, bitwise operations, structure, and ternary operators. The interpreter is also buggy and does not catch errors. Even though there are commands called "if" and "for", they are just special jump statements and do not provide any structure to the code.

# Poklang++
Poklang++ is a lightweight, static, imperative, structured programming language. It is the improved version of Poklang. I did not finish the interpreter yet.
