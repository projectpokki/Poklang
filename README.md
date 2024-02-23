# WARNING
There are lots of bugs in this interpreter. I forgot how this language actually works, so there will never be actual documentation. Instead I uploaded some notes I wrote down while designing the language. While making this project, I noticed many places for improvement that would basically require restarting. So this project will not be completed and instead I will completely restart and make a better, and more advanced, language and interpreter: Poklang++. 

# Poklang
Poklang is a lightweight imperative programming language. It revolves around variable manipulation and commands. There are 31 commands in Poklang, and these commands allow you to do basic mathematical operations, string manipulation, I/O and boolean logic. Poklang is able to do most simple tasks that only require access to the console.
# Setting Up Interpreter
There are 4 python files and 1 text life - ```main.py```, ```LexerModule.py```, ```ParserModule.py```, ```ExecutorModule.py```, and ```Poklang.txt```. They work together to interpret and run text as code. If you want to change the name of the Poklang file, you need to change the value of ```fileName``` in line 1 of ```main.py```. By default, it is set to "Poklang.txt".<br><br>An alternative to running the 4 python files is running ```PoklangInterpreter.py```, which is all 4 files joined together as one.
