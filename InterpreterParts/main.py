fileName = "Poklang.txt" #set this variable to the name of the Poklang file you are running.

import ExecutorModule as e
import LexerModule as l
import ParserModule as p
e.runCode(p.parse(l.tokenize(fileName)))
