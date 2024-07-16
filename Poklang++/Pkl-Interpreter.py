import math
from copy import deepcopy
from os.path import exists
from time import sleep, time

fileToRun = ""


#functions and resources
parserLineNumber = 0
execLineNumber = [0]
varIDs = {}
vars: list = []
consts = {}
funcs = {}
startingLine = -1

parserErrorText: list = [
    "instruction is malformed", "pointer does not exist", "malformed token",
    "token has invalid type", "file does not exist or is in invalid format",
    "instruction does not exist", "negative indentation",
    "name of pointer or constant is already used",
    "loop or condition not closed properly",
    "main code block already initialised",
    "instruction cannot used outside code block or does not exist",
    "constant or variable is declared after main code block"
]

runtimeErrorText: list = [
    "index has invalid range", "attempt to wait for negative time",
    "attempt to create array with negative length",
    "input outside domain of math function",
    "division by 0, output is undefined", "pointer has no value",
    "reached end of file but program is not ended",
    "attempt to give a pointer a value of different type",
    "attempt to convert non-numeric string to int or float"
]

types: list = ["int", "float", "bool", "char", "arr", "str"]


def printParserError(errorType):
  print("PARSING ERROR - LINE " + str(parserLineNumber + 1) + ": " +
        parserErrorText[errorType])
  exit()


def printRuntimeError(errorType):
  print("RUNTIME ERROR - LINE " + str(parserLineNumber + 1) + ": " +
        runtimeErrorText[errorType])
  exit()


def encodeVar(var):
  if var in varIDs:
    return varIDs[var]
  return None


def encodeVarOrConst(input):
  if input in varIDs:
    return varIDs[input]
  elif input in consts:
    return consts[input]
  elif input == "null":
    return "cn"
  elif input == "true":
    return "cb1"
  elif input == "false":
    return "cb0"
  elif input[0] == "\"" and input[-1] == "\"":
    input = input.replace("\\n", "\n")
    input = input.replace("\\t", "\t")
    input = input.replace("\\b", "\b")
    input = input.replace("\\\\", "\\")
    if len(input) > 3:
      return "cs" + input[1:-1]
    else:
      return "cc" + input[1:-1]
  try:
    return "ci" + str(int(input))
  except ValueError:
    try:
      return "cf" + str(float(input))
    except ValueError:
      return None


def getValue(input):
  if input[0] == "v":
    if vars[int(input[2:])] is None:
      printRuntimeError(5)
    return vars[int(input[2:])]  #variable and array
  elif input[1] == "n":
    return None
  elif input[1] == "i":
    return int(input[2:])  #const int
  elif input[1] == "f":
    return float(input[2:])  #const float
  elif input[1] == "b" and input[2] == "1":
    return True  #const bool
  elif input[1] == "b" and input[2] == "0":
    return False
  elif input[1] == "c" and input != "cc":
    return input[2]  #const char
  elif input[1] == "s":
    return input[2:]  #const str
  else:
    return ""


def getNumberValue(input):
  if input[0] == "v":
    if vars[int(input[2:])] is None:
      printRuntimeError(5)
    return float(vars[int(input[2:])])
  return float(input[2:])


def getBoolValue(input):
  if input[0] == "v":
    if varIDs[int(input[2:])] is None:
      printRuntimeError(5)
    return bool(varIDs[int(input[2:])])
  if input[2] == "1":
    return True
  return False


def canOpenFile(fileName):
  if not exists(fileName):
    return False
  try:
    with open(fileName) as file:
      file.read()
  except UnicodeDecodeError:
    return False
  return True

#set file
newFile = ""
with open(__file__, "r") as selfR:
  lines = selfR.read().split("\n")
  if lines[3] == "" or not exists(fileToRun):
    print("[POKLANG++ INTERPRETER SETTINGS]")
    fileToRunInput = input("Enter name of file to run: ")
    if not exists(fileToRunInput):
      print(
          "File to run does not exist. Restart program to change file to run.")
      exit()
    newLine = "fileToRun = \"" + fileToRunInput + "\""
    newFile = "\n".join(lines[:6] + [newLine] + lines[7:])
    selfR.close()
    with open(__file__, "w") as selfW:
      selfW.write(newFile)
      print("File set successfully. Restart program to run " + fileToRunInput + ".")
      exit()

#interpret file
with open(fileToRun, "r") as code:
  #format
  formattedCode = []
  for line in code.read().splitlines():
    formattedLine = []
    for sectNum, sect in enumerate(line.split("#")[0].strip().split("\"")):
      if sectNum % 2 == 1:
        formattedLine.append("\"" + sect + "\"")
      else:
        formattedLine += sect.split()
    formattedCode.append(formattedLine)
  
  #parse file
  indentationLevel = 0
  indentationType = [""]
  loopStartLocations = [0]

  for lineNum, line in enumerate(code):
    if line[0] == "func":
      funcs[line[1]] = lineNum

  for parserLineNumber, line in enumerate(formattedCode):
    if line == []:
      continue

    #outside code block
    if indentationLevel == 0:
      if line[0] == "const":
        if line[1] in types:
          if line[1] == "arr" and len(line) >= 5:
            pass 
          elif line[1] != "arr" and len(line) == 5:
            if startingLine != -1: printParserError(11)
            if line[2] in consts or line[2] in varIDs or line[2] in funcs: printParserError(7)
            consts[line[2]] = encodeVarOrConst(line[4])
            if consts[line[2]] is None: printParserError(2)
            if consts[line[2]][1] != line[1][0]: printParserError(3)
            formattedCode[parserLineNumber] = []
            continue
          else: printParserError(0)
  
      elif line[0] == "var":
        if line[1] in types and len(line) >= 3:
          if startingLine != -1: printParserError(11)
          for i in range(2, len(line)):
            if line[i] in consts or line[i] in varIDs or line[i] in funcs:
              printParserError(7)
            varIDs[line[i]] = "v" + line[1][0] + str(len(varIDs))
          formattedCode[parserLineNumber] = []
          continue
        else: printParserError(0)
      
      elif line[0] == "func":
        if len(line) == 2:
          if line[1] in consts or line[1] in varIDs: printParserError(7)
          indentationType[0] = "func"
          indentationLevel = 1
          formattedCode[parserLineNumber] = []
          continue
        else: printParserError(0)
  
      elif line[0] == "start":
        if startingLine >= 0: printParserError(9)
        if len(line) == 1:
          indentationType[0] = "main"
          startingLine = parserLineNumber
          indentationLevel = 1
          formattedCode[parserLineNumber] = []
          continue
        else: printParserError(0)
  
      else:
        printParserError(10)

    #Var
    elif line[0] == "set":
      if line[2] == "<" and len(line) == 4:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[1][1] != line[2][1]: printParserError(3)
        line.pop(3)
      else: printParserError(0)

    #IO/time
    elif line[0] == "stdin":
      if len(line) == 2:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != "s": printParserError(3)
      else: printParserError(0)

    elif line[0] == "stdout":
      if len(line) >= 2:
        for i in range(1, len(line)):
          line[i] = encodeVarOrConst(line[i])
          if line[i] is None: printParserError(2)
      else: printParserError(0)

    elif line[0] == "filein":
      if len(line) == 3:
        line[1] = encodeVarOrConst(line[1])
        if line[1] is None: printParserError(2)
        if line[1][1] != "s": printParserError(3)
        if not canOpenFile(line[1][2:]): printParserError(4)
        line[2] = encodeVar(line[2])
        if line[2] is None: printParserError(1)
        if line[2][1] != "s": printParserError(3)
      else: printParserError(0)

    elif line[0] == "fileout":
      if len(line) >= 2:
        line[1] = encodeVarOrConst(line[1])
        if line[1] is None: printParserError(2)
        if line[1][1] != "s": printParserError(3)
        if not canOpenFile(line[1][2:]): printParserError(4)
        for i in range(2, len(line)):
          line[i] = encodeVarOrConst(line[i])
          if line[i] is None: printParserError(2)
      else: printParserError(0)

    elif line[0] == "fileclear":
      if len(line) == 2:
        line[1] = encodeVarOrConst(line[1])
        if line[1] is None: printParserError(2)
        if line[1][1] != "s": printParserError(3)
        if not canOpenFile(line[1][2:]): printParserError(4)
      else: printParserError(0)

    elif line[0] in ["unixtime", "exectime"]:
      if len(line) == 2:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != "f": printParserError(3)
      else: printParserError(0)

    elif line[0] == "wait":
      if len(line) == 2:
        line[1] = encodeVarOrConst(line[1])
        if line[1] is None: printParserError(2)
        if line[1][1] not in ["i", "f"]: printParserError(3)
      else: printParserError(0)

    #Arr/str
    elif line[0] == "setarr":
      if line[2] == "<" and len(line) >= 4:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != "a": printParserError(3)
        for i in range(2, len(line) - 1):
          line[i] = encodeVarOrConst(line[i + 1])
          if line[i] is None: printParserError(2)
        line.pop(-1)
      else: printParserError(0)

    elif line[0] == "append":
      if line[2] == "<" and len(line) == 4:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != "a": printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        line.pop(3)
      else: printParserError(0)

    elif line[0] == "conc":
      if line[2] == "<" and len(line) == 5:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] not in ["a", "s"]: printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        line[3] = encodeVarOrConst(line[4])
        if line[3] is None: printParserError(2)
        if line[1][1] == "s" and (line[2][1] not in ["c", "s"] or line[3][1] not in ["c", "s"]): printParserError(3)
        if line[1][1] == "a" and (line[2][1] != "a" or line[3][1] != "a"): printParserError(3)
        line.pop(4)
      else: printParserError(0)

    elif line[0] == "remove":
      if len(line) == 3:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] not in ["a", "s"]: printParserError(3)
        line[2] = encodeVarOrConst(line[2])
        if line[2] is None: printParserError(2)
        if line[2][1] != "i": printParserError(3)
      else: printParserError(0)

    elif line[0] == "indset":
      if line[3] == "<" and len(line) == 5:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] not in ["a", "s"]: printParserError(3)
        line[2] = encodeVarOrConst(line[2])
        if line[2] is None: printParserError(2)
        if line[2][1] != "i": printParserError(3)
        line[3] = encodeVarOrConst(line[4])
        if line[3] is None: printParserError(2)
        if line[1][1] == "s" and line[3][1] != "c": printParserError(3)
        line.pop(4)
      else: printParserError(0)

    elif line[0] == "indget":
      if line[2] == "<" and len(line) == 5:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] not in ["a", "s"]: printParserError(3)
        if line[2][1] == "s" and line[1][1] != "c": printParserError(3) 
        line[3] = encodeVarOrConst(line[4])
        if line[3] is None: printParserError(2)
        if line[3][1] != "i": printParserError(3)
        line.pop(4)
      else: printParserError(0)

    elif line[0] == "split":
      if line[2] == "<" and len(line) == 6:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] not in ["a", "s"]: printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] != line[1][1]: printParserError(3)
        line[3] = encodeVarOrConst(line[4])
        if line[3] is None: printParserError(2)
        if line[3][1] != "i": printParserError(3)
        line[4] = encodeVarOrConst(line[5])
        if line[4] is None: printParserError(2)
        if line[4][1] != "i": printParserError(3)
        line.pop(5)
      else: printParserError(0)

    elif line[0] == "len":
      if line[2] == "<" and len(line) == 4:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != "i": printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] not in ["a", "s", "c"]: printParserError(3)
        line.pop(3)
      else: printParserError(0)

    elif line[0] == "forcelen":
      if line[2] == "<" and len(line) == 4:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != "a": printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] != "i": printParserError(3)
        line.pop(3)
      else: printParserError(0)

    #Types
    elif line[0] == "hex":
      if line[2] == "<" and len(line) == 4:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] not in ["s", "c"]: printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] != "i": printParserError(3)
        line.pop(3)
      else: printParserError(0)

    elif line[0] == "dec":
      if line[2] == "<" and len(line) == 4:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != "i": printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] != "s": printParserError(3)
        line.pop(3)
      else: printParserError(0)

    elif line[0] == "type":
      if line[2] == "<" and len(line) == 4:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != "s": printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        line[2] = line[2][1]
        line.pop(3)
      else: printParserError(0)

    elif line[0] in ["itof", "ftoi", "itos", "stoi", "ftos", "stof", "itoc", "ctoi", "ctos", "stoc"]:
      if line[2] == "<" and len(line) == 4:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != line[0][3]: printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] != line[0][0]: printParserError(3)
        line.pop(3)
      else: printParserError(0)

    elif line[0] == "tochar":
      if line[2] == "<" and len(line) == 4:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != "c": printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] != "i": printParserError(3)
        line.pop(3)
      else: printParserError(0)

    elif line[0] == "toint":
      if line[2] == "<" and len(line) == 4:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != "i": printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] != "c": printParserError(3)
        line.pop(3)
      else: printParserError(0)

    #Math 2 Inputs
    elif line[0] in ["sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "asinh", "acosh", "atanh", "abs", "floor", "ceil", "rad", "deg"]:
      if line[2] == "<" and len(line) == 4:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] not in ["i", "f"]: printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] not in ["i", "f"]: printParserError(3)
        line.pop(3)
      else: printParserError(0)

    #Math 1 Input
    elif line[0] in ["add", "sub", "mul", "div", "mod", "exp", "log", "max", "min"]:
      if line[2] == "<" and len(line) == 5:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] not in ["i", "f"]: printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] not in ["i", "f"]: printParserError(3)
        line[3] = encodeVarOrConst(line[4])
        if line[3] is None: printParserError(2)
        if line[3][1] not in ["i", "f"]: printParserError(3)
        line.pop(4)
      else: printParserError(0)

    #Bitwise
    elif line[0] in ["intand", "intor", "intxor", "intnand", "intnor", "intxnor"]:
      if line[2] == "<" and len(line) == 5:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != "i": printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] != "i": printParserError(3)
        line[3] = encodeVarOrConst(line[4])
        if line[3] is None: printParserError(2)
        if line[3][1] != "i": printParserError(3)
        line.pop(4)
      else: printParserError(0)

    elif line[0] == "intnot":
      if line[2] == "<" and len(line) == 4:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != "i": printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] != "i": printParserError(3)
        line.pop(3)
      else: printParserError(0)

    #Bool
    elif line[0] in ["and", "or", "xor", "nand", "nor", "xnor"]:
      if line[2] == "<" and len(line) == 5:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != "b": printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] != "b": printParserError(3)
        line[3] = encodeVarOrConst(line[4])
        if line[3] is None: printParserError(2)
        if line[3][1] != "b": printParserError(3)
        line.pop(4)
      else: printParserError(0)

    elif line[0] == "not":
      if line[2] == "<" and len(line) == 4:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != "b": printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] != "b": printParserError(3)
        line.pop(3)
      else: printParserError(0)

    elif line[0] in ["less", "grt", "gequ", "lequ"]:
      if line[2] == "<" and len(line) == 5:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != "b": printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] not in ["i", "f"]: printParserError(3)
        line[3] = encodeVarOrConst(line[4])
        if line[3] is None: printParserError(2)
        if line[3][1] not in ["i", "f"]: printParserError(3)
        line.pop(4)
      else: printParserError(0)

    elif line[0] in ["equ", "nequ"]:
      if line[2] == "<" and len(line) == 5:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] != "b": printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[1] is None: printParserError(2)
        line[3] = encodeVarOrConst(line[4])
        if line[1] is None: printParserError(2)
        line.pop(4)
      else: printParserError(0)

    #Control
    elif line[0] == "if":
      if len(line) == 2:
        line[1] = encodeVarOrConst(line[1])
        if line[1] is None: printParserError(2)
        if line[1][1] != "b": printParserError(3)
        if indentationLevel >= len(indentationType):
          indentationType.append("if")
        else:
          indentationType[indentationLevel] = "if"
        indentationLevel += 1
        line.append(indentationLevel)
      else: printParserError(0)

    elif line[0] == "elseif":
      if indentationType[indentationLevel - 1] != "if": printParserError(8)
      if len(line) == 2:
        line[1] = encodeVarOrConst(line[1])
        if line[1] is None: printParserError(2)
        if line[1][1] != "b": printParserError(3)
        line.append(indentationLevel)
      else: printParserError(0)

    elif line[0] == "switch":
      if len(line) == 2:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if indentationLevel >= len(indentationType):
          indentationType.append("switch")
        else:
          indentationType[indentationLevel] = "switch"
        indentationLevel += 1
        line.append(indentationLevel)
      else: printParserError(0)

    elif line[0] == "case":
      if indentationType[indentationLevel - 1] != "switch": printParserError(8)
      if len(line) == 2:
        line[1] = encodeVarOrConst(line[1])
        if line[1] is None: printParserError(2)
        line.append(indentationLevel)
      else: printParserError(0)

    elif line[0] == "else":
      if indentationType[indentationLevel - 1] not in ["if", "switch"]: printParserError(8)
      if len(line) == 1:
        line.append(indentationLevel)
      else: printParserError(0)

    elif line[0] == "endcond":
      if indentationLevel <= 0: printParserError(6)
      if indentationType[indentationLevel - 1] not in ["if", "switch"]: printParserError(8)
      if len(line) == 1:
        line.append(indentationLevel)
        indentationLevel -= 1
      else: printParserError(0)

    elif line[0] == "while":
      if len(line) == 2:
        line[1] = encodeVarOrConst(line[1])
        if line[1] is None: printParserError(2)
        if line[1][1] != "b": printParserError(3)
        if indentationLevel >= len(indentationType):
          indentationType.append("loop")
        else:
          indentationType[indentationLevel] = "loop"
        indentationLevel += 1
        line.append(indentationLevel)
        if indentationLevel >= len(loopStartLocations):
          loopStartLocations.append(parserLineNumber)
        else:
          loopStartLocations[indentationLevel] = parserLineNumber
      else: printParserError(0)

    elif line[0] == "for":
      if line[2] == "<" and len(line) == 6:
        line[1] = encodeVar(line[1])
        if line[1] is None: printParserError(1)
        if line[1][1] not in ["i", "f"]: printParserError(3)
        line[2] = encodeVarOrConst(line[3])
        if line[2] is None: printParserError(2)
        if line[2][1] not in ["i", "f"]: printParserError(3)
        line[3] = encodeVarOrConst(line[4])
        if line[3] is None: printParserError(2)
        if line[3][1] not in ["i", "f"]: printParserError(3)
        line[4] = encodeVarOrConst(line[5])
        if line[4] is None: printParserError(2)
        if line[4][1] not in ["i", "f"]: printParserError(3)
        line.pop(5)
        if indentationLevel + 1 >= len(indentationType):
          indentationType.append("loop")
        else:
          indentationType[indentationLevel] = "loop"
        indentationLevel += 1
        line.append(indentationLevel)
        if indentationLevel >= len(loopStartLocations):
          loopStartLocations.append(parserLineNumber)
        else:
          loopStartLocations[indentationLevel] = parserLineNumber
      else: printParserError(0)

    elif line[0] in ["break", "continue"]:
      inLoopNest = False
      for layer in range(indentationLevel - 1, -1, -1):
        if indentationType[layer] == "loop":
          line.append(layer + 1)
          inLoopNest = True
          break
      if not inLoopNest: printParserError(8)
      if len(line) == 2: #1 element input, but appended extra int at end
        line.append(indentationLevel)
      else: printParserError(0)

    elif line[0] == "endloop":
      if indentationLevel <= 0: printParserError(6)
      if indentationType[indentationLevel - 1] != "loop": printParserError(8)
      if len(line) == 1:
        line.append(loopStartLocations[indentationLevel - 1])
        line.append(indentationLevel)
        indentationLevel -= 1
      else: printParserError(0)

    #Function
    elif line[0] == "endfunc":
      if indentationLevel != 1 or indentationType[0] != "func": printParserError(8)
      if len(line) == 1:
        indentationLevel = 0
      else: printParserError(0)

    elif line[0] == "runfunc":
      if len(line) == 2:
        if line[1] not in funcs: printParserError(1)
        line[1] = funcs[line[1]]
      else: printParserError(0)

    elif line[0] == "return":
      if indentationType[0] != "func": printParserError(10)
      if len(line) != 1:
        printParserError(0)

    elif line[0] == "end":
      if indentationLevel != 1 or indentationType[0] != "main": printParserError(8)
      if len(line) == 1:
        indentationLevel = 0
      else: printParserError(0)

    elif line[0] == "quit":
      if len(line) != 1: printParserError(0)

    elif line[0] in ["func", "start", "var", "const"]:
      printParserError(10)
    else:
      printParserError(5)

  if indentationLevel != 0:
    printParserError(8)
  
  #run file
  executionStartTime = time()
  parserLineNumber = startingLine
  vars = [None] * len(varIDs)
  controlState = [0]
  indentation = [1]
  functionLayer = 0
  switchVariable = [None]

  while True:
    if execLineNumber[functionLayer] >= len(formattedCode):
      printRuntimeError(6)
    line = formattedCode[execLineNumber[functionLayer]]

    if line == []:
      execLineNumber[functionLayer] += 1
      continue
    
    if controlState[functionLayer] == 0:
      #Variable
      if line[0] == "set":
        if line[2][1] == "a":
          vars[int(line[1][2:])] = deepcopy(getValue(line[2]))
        else:
          vars[int(line[1][2:])] = getValue(line[2])

      #IO/time
      elif line[0] == "stdin":
        vars[int(line[1][2:])] = input()

      elif line[0] == "stdout":
        for i in line[1:]:
          string = getValue(i)
          if string is True:
            print("true", end="")
          elif string is False:
            print("false", end="")
          elif isinstance(string, list):
            for i in string:
              print(i, end="")
          elif string is not None:
            print(string, end="")

      elif line[0] == "filein":
        with open(line[1][2:], mode="r") as file:
          vars[int(line[2][2:])] = file.read()
          file.close()

      elif line[0] == "fileout":
        with open(line[1][2:], mode="a") as file:
          for i in line[2:]:
            file.write(str(getValue(i)))
          file.close()

      elif line[0] == "fileclear":
        with open(line[1][2:], mode="w") as file:
          file.write("")
        file.close()

      elif line[0] == "unixtime":
        vars[int(line[1][2:])] = time()

      elif line[0] == "exectime":
        vars[int(line[1][2:])] = time() - executionStartTime

      elif line[0] == "wait":
        waittime = getNumberValue(line[1])
        if waittime >= 0:
          sleep(0.001 * waittime)
        else:
          printRuntimeError(1)
      
      #Arr/str
      elif line[0] == "setarr":
        vars[int(line[1][2:])] = []
        for i in line[2:]:
          vars[int(line[1][2:])].append(getValue(i))

      elif line[0] == "append":
        vars[int(line[1][2:])].append(getValue(line[2]))

      elif line[0] == "conc":
        if line[1][1] == "a":
          #ignore type error
          vars[int(line[1][2:])] = deepcopy(getValue(line[2])) + deepcopy(getValue(line[3]))
        else:
          vars[int(line[1][2:])] = str(getValue(line[2])) + str(getValue(line[3]))

      elif line[0] == "remove":
        index = getNumberValue(line[2])
        if index <= len(vars[int(line[1][2:])]) - 1 and index >= 0:
          vars[int(line[1][2:])].pop(getValue(line[2]))
        else:
          printRuntimeError(0)

      elif line[0] == "indset":
        index = getNumberValue(line[2])
        if index <= len(vars[int(line[1][2:])]) - 1 and index >= 0:
          if line[1][1] == "a":
            vars[int(line[1][2:])][getValue(line[2])] = getValue(line[3])
          else:
            vars[int(line[1][2:])] = list(vars[int(line[1][2:])])
            vars[int(line[1][2:])][getValue(line[2])] = getValue(line[3])
            vars[int(line[1][2:])] = "".join(vars[int(line[1][2:])])
        else:
          printRuntimeError(0)

      elif line[0] == "indget": #"int", "float", "bool", "char", "arr", "str"
        index = int(getNumberValue(line[3]))
        if index <= len(getValue(line[2])) - 1 and index >= 0:
          indexValue = getValue(line[2])[index]
          if (isinstance(indexValue, int) and line[1][1] == "i") or (isinstance(indexValue, float) and line[1][1] == "f") or (isinstance(indexValue, bool) and line[1][1] == "b"):
            vars[int(line[1][2:])] = indexValue
          elif isinstance(indexValue, str) and line[1][1] == "c":
            if len(indexValue) == 1:
              vars[int(line[1][2:])] = indexValue
            else:
              printRuntimeError(7)
          elif isinstance(indexValue, list) and line[1][1] == "a":
            vars[int(line[1][2:])] = deepcopy(indexValue)
          elif isinstance(indexValue, str) and line[1][1] == "s":
            vars[int(line[1][2:])] = indexValue
          else:
            printRuntimeError(7)
        else:
          printRuntimeError(0)

      elif line[0] == "split":
        minIndex = int(getNumberValue(line[3]))
        maxIndex = int(getNumberValue(line[4])) + 1
        if minIndex <= len(getValue(line[2])) - 1 and minIndex >= 0 and maxIndex <= len(getValue(line[2])) and maxIndex >= 1 and maxIndex >= minIndex + 1:
          if line[2][1] == "a":
            vars[int(line[1][2:])] = deepcopy(getValue(line[2]))[minIndex:maxIndex]
          else:
            vars[int(line[1][2:])] = getValue(line[2])[minIndex:maxIndex]
        else:
          printRuntimeError(0)

      elif line[0] == "len":
        vars[int(line[1][2:])] = len(getValue(line[2]))

      elif line[0] == "forcelen":
        length = int(getNumberValue(line[2]))
        if length >= 0:
          if length < len(vars[int(line[1][2:])]):
            vars[int(line[1][2:])] = deepcopy(vars[int(line[1][2:])])[:length]
          elif length > len(vars[int(line[1][2:])]):
            vars[int(line[1][2:])] = vars[int(line[1][2:])] + [None] * int(length - len(vars[int(line[1][2:])]))
        else:
          printRuntimeError(2)

      #Types
      elif line[0] == "hex":
        vars[int(line[1][2:])] = hex(int(getNumberValue(line[2])))
        if line[1][1] == "c": vars[int(line[1][2:])] = vars[int(line[1][2:])][-1]

      elif line[0] == "dec":
        hexStr = str(getValue(line[2]))
        if hexStr[:2] == "0x":
          vars[int(line[1][2:])] = int(hexStr, 16)
        else: printRuntimeError(8)

      elif line[0] == "type":
        if line[2] == "i": vars[int(line[1][2:])] = "int"
        elif line[2] == "f": vars[int(line[1][2:])] = "float"
        elif line[2] == "b": vars[int(line[1][2:])] = "bool"
        elif line[2] == "c": vars[int(line[1][2:])] = "char"
        elif line[2] == "a": vars[int(line[1][2:])] = "arr"
        elif line[2] == "s": vars[int(line[1][2:])] = "str"

      elif line[0] == "itof":
        vars[int(line[1][2:])] = float(getNumberValue(line[2]))

      elif line[0] == "ftoi":
        vars[int(line[1][2:])] = int(getNumberValue(line[2]))

      elif line[0] == "itos":
        vars[int(line[1][2:])] = str(getNumberValue(line[2]))

      elif line[0] == "stoi":
        try:
          vars[int(line[1][2:])] = int(getValue(line[2]))
        except ValueError:
          printRuntimeError(8)

      elif line[0] == "ftos":
        vars[int(line[1][2:])] = str(getNumberValue(line[2]))

      elif line[0] == "stof":
        try:
          vars[int(line[1][2:])] = float(getValue(line[2]))
        except ValueError:
          printRuntimeError(8)

      elif line[0] == "itoc":
        vars[int(line[1][2:])] = str(getNumberValue(line[2]))[-1]

      elif line[0] == "ctoi":
        try:
          vars[int(line[1][2:])] = float(str(getValue(line[2]))[-1])
        except ValueError:
          printRuntimeError(8)

      elif line[0] == "ctos":
        vars[int(line[1][2:])] = str(getValue(line[2]))

      elif line[0] == "stoc":
        vars[int(line[1][2:])] = str(getValue(line[2]))[-1]

      elif line[0] == "tochar":
        vars[int(line[1][2:])] = chr(int(getNumberValue(line[2])))

      elif line[0] == "toint":
        vars[int(line[1][2:])] = ord(str(getValue(line[2])))

      #Math - trig
      elif line[0] == "sin":
        vars[int(line[1][2:])] = math.sin(getNumberValue(line[2]))
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      elif line[0] == "cos":
        vars[int(line[1][2:])] = math.cos(getNumberValue(line[2]))
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      elif line[0] == "tan":
        vars[int(line[1][2:])] = math.tan(getNumberValue(line[2]))
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      elif line[0] == "asin":
        if getNumberValue(line[2]) <= 1 and getNumberValue(line[2]) >= -1:
          vars[int(line[1][2:])] = math.asin(getNumberValue(line[2]))
          if line[1][1] == "i":
            vars[int(line[1][2:])] = int(vars[int(line[1][2:])])
        else:
          printRuntimeError(3)

      elif line[0] == "acos":
        if getNumberValue(line[2]) <= 1 and getNumberValue(line[2]) >= -1:
          vars[int(line[1][2:])] = math.acos(getNumberValue(line[2]))
          if line[1][1] == "i":
            vars[int(line[1][2:])] = int(vars[int(line[1][2:])])
        else:
          printRuntimeError(3)

      elif line[0] == "atan":
        vars[int(line[1][2:])] = math.atan(getNumberValue(line[2]))
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      elif line[0] == "sinh":
        vars[int(line[1][2:])] = math.sinh(getNumberValue(line[2]))
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      elif line[0] == "cosh":
        vars[int(line[1][2:])] = math.cosh(getNumberValue(line[2]))
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      elif line[0] == "tanh":
        vars[int(line[1][2:])] = math.tanh(getNumberValue(line[2]))
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      elif line[0] == "asinh":
        vars[int(line[1][2:])] = math.asinh(getNumberValue(line[2]))
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      elif line[0] == "acosh":
        if getNumberValue(line[2]) >= 1:
          vars[int(line[1][2:])] = math.acosh(getNumberValue(line[2]))
          if line[1][1] == "i":
            vars[int(line[1][2:])] = int(vars[int(line[1][2:])])
        else:
          printRuntimeError(3)

      elif line[0] == "atanh":
        if getNumberValue(line[2]) < 1 and getNumberValue(line[2]) > -1:
          vars[int(line[1][2:])] = math.atanh(getNumberValue(line[2]))
          if line[1][1] == "i":
            vars[int(line[1][2:])] = int(vars[int(line[1][2:])])
        else:
          printRuntimeError(3)

      #Math - one input
      elif line[0] == "abs":
        vars[int(line[1][2:])] = math.fabs(getNumberValue(line[2]))
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      elif line[0] == "floor":
        vars[int(line[1][2:])] = math.floor(getNumberValue(line[2]))
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      elif line[0] == "ceil":
        vars[int(line[1][2:])] = math.ceil(getNumberValue(line[2]))
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      elif line[0] == "rad":
        vars[int(line[1][2:])] = 0.017453292519943295 * getNumberValue(line[2])
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      elif line[0] == "deg":
        vars[int(line[1][2:])] = 57.29577951308232 * getNumberValue(line[2])
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      #Math - two inputs
      elif line[0] == "add":
        vars[int(line[1][2:])] = getNumberValue(line[2]) + getNumberValue(line[3])
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      elif line[0] == "sub":
        vars[int(line[1][2:])] = getNumberValue(line[2]) - getNumberValue(line[3])
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      elif line[0] == "mul":
        vars[int(line[1][2:])] = getNumberValue(line[2]) * getNumberValue(line[3])
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      elif line[0] == "div":
        if getNumberValue(line[3]) != 0:
          vars[int(line[1][2:])] = getNumberValue(line[2]) / getNumberValue(line[3])
          if line[1][1] == "i":
            vars[int(line[1][2:])] = int(vars[int(line[1][2:])])
        else:
          printRuntimeError(4)

      elif line[0] == "mod":
        if getNumberValue(line[3]) != 0:
          vars[int(line[1][2:])] = getNumberValue(line[2]) % getNumberValue(line[3])
          if line[1][1] == "i":
            vars[int(line[1][2:])] = int(vars[int(line[1][2:])])
        else:
          printRuntimeError(4)

      elif line[0] == "exp":  #note: 0^0=1 for python
        if getNumberValue(line[2]) != 0 and getNumberValue(line[3]) != 0:
          vars[int(line[1][2:])] = getNumberValue(line[2])**getNumberValue(line[3])
          if line[1][1] == "i":
            vars[int(line[1][2:])] = int(vars[int(line[1][2:])])
        else:
          printRuntimeError(4)

      elif line[0] == "log":
        if getNumberValue(line[2]) > 0 and getNumberValue(line[3]) > 0:
          if getNumberValue(line[3]) == 1: printRuntimeError(4)
          vars[int(line[1][2:])] = math.log(getNumberValue(line[2]), getNumberValue(line[3]))
          if line[1][1] == "i":
            vars[int(line[1][2:])] = int(vars[int(line[1][2:])])
        else:
          printRuntimeError(3)

      elif line[0] == "min":
        vars[int(line[1][2:])] = min(getNumberValue(line[2]), getNumberValue(line[3]))
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      elif line[0] == "max":
        vars[int(line[1][2:])] = max(getNumberValue(line[2]), getNumberValue(line[3]))
        if line[1][1] == "i":
          vars[int(line[1][2:])] = int(vars[int(line[1][2:])])

      #Bitwise
      elif line[0] == "intand":
        vars[int(line[1][2:])] = int(getNumberValue(line[2])) & int(getNumberValue(line[3]))

      elif line[0] == "intor":
        vars[int(line[1][2:])] = int(getNumberValue(line[2])) | int(getNumberValue(line[3]))

      elif line[0] == "intxor":
        vars[int(line[1][2:])] = int(getNumberValue(line[2])) ^ int(getNumberValue(line[3]))

      elif line[0] == "intnand":
        vars[int(line[1][2:])] = ~(int(getNumberValue(line[2])) & int(getNumberValue(line[3])))

      elif line[0] == "intnor":
        vars[int(line[1][2:])] = ~(int(getNumberValue(line[2])) | int(getNumberValue(line[3])))

      elif line[0] == "intxnor":
        vars[int(line[1][2:])] = ~(int(getNumberValue(line[2])) ^ int(getNumberValue(line[3])))

      elif line[0] == "intnot":
        vars[int(line[1][2:])] = ~(int(getNumberValue(line[2])))

      #Bool
      elif line[0] == "and":
        vars[int(line[1][2:])] = getBoolValue(line[2]) and getBoolValue(line[3])

      elif line[0] == "or":
        vars[int(line[1][2:])] = getBoolValue(line[2]) or getBoolValue(line[3])

      elif line[0] == "xor":
        vars[int(line[1][2:])] = getBoolValue(line[2]) ^ getBoolValue(line[3])

      elif line[0] == "nand":
        vars[int(line[1][2:])] = not (getBoolValue(line[2]) and getBoolValue(line[3]))

      elif line[0] == "nor":
        vars[int(line[1][2:])] = not (getBoolValue(line[2]) or getBoolValue(line[3]))

      elif line[0] == "xnor":
        vars[int(line[1][2:])] = not (getBoolValue(line[2]) ^ getBoolValue(line[3]))

      elif line[0] == "not":
        vars[int(line[1][2:])] = not getBoolValue(line[2])

      elif line[0] == "less":
        vars[int(line[1][2:])] = getNumberValue(line[2]) < getNumberValue(line[3])

      elif line[0] == "grt":
        vars[int(line[1][2:])] = getNumberValue(line[2]) > getNumberValue(line[3])

      elif line[0] == "lequ":
        vars[int(line[1][2:])] = getNumberValue(line[2]) <= getNumberValue(line[3])

      elif line[0] == "gequ":
        vars[int(line[1][2:])] = getNumberValue(line[2]) >= getNumberValue(line[3])

      elif line[0] == "equ":
        vars[int(line[1][2:])] = getNumberValue(line[2]) == getNumberValue(line[3])

      elif line[0] == "nequ":
        vars[int(line[1][2:])] = getNumberValue(line[2]) != getNumberValue(line[3])

      #Control (dark magic structured programming)
      elif line[0] == "if" and line[-1] == indentation[functionLayer] + 1:
        if getBoolValue(line[1]):
          controlState[functionLayer] = 0
        else:
          controlState[functionLayer] = 1
        indentation[functionLayer] += 1
  
      elif line[0] in ["elif", "case", "else"] and line[-1] == indentation[functionLayer]:
        controlState[functionLayer] = 3
  
      elif line[0] == "endcond" and line[-1] == indentation[functionLayer]:
        indentation[functionLayer] -= 1
  
      elif line[0] == "switch" and line[-1] == indentation[functionLayer] + 1:
        switchVariable[functionLayer] = getValue(line[1])
        controlState[functionLayer] = 2
        indentation[functionLayer] += 1
  
      elif line[0] == "while" and line[-1] == indentation[functionLayer] + 1:
        if getBoolValue(line[1]):
          controlState[functionLayer] = 0
        else:
          controlState[functionLayer] = 5
        indentation[functionLayer] += 1
  
      elif line[0] == "for" and line[-1] == indentation[functionLayer] + 1:
        vars[int(line[1][2:])] = getNumberValue(line[2]) #first time
        if line[1][1] == "i": vars[int(line[1][2:])] = int(vars[int(line[1][2:])])
        if (getNumberValue(line[4]) >= 0 and vars[int(line[1][2:])] <= getNumberValue(line[3])) or (getNumberValue(line[4]) < 0 and vars[int(line[1][2:])] >= getNumberValue(line[3])):
          controlState[functionLayer] = 0
        else:
          controlState[functionLayer] = 5
        indentation[functionLayer] += 1
  
      elif line[0] == "break" and line[-1] == indentation[functionLayer]:
        controlState[functionLayer] = 5
        indentation[functionLayer] = line[1]
  
      elif line[0] == "continue" and line[-1] == indentation[functionLayer]:
        controlState[functionLayer] = 4
  
      elif line[0] == "endloop" and line[-1] == indentation[functionLayer]:
        controlState[functionLayer] = 4
        execLineNumber[functionLayer] = line[1] #jump back to start of loop
        indentation[functionLayer] -= 1
        continue
  
      elif line[0] == "runfunc":
        functionLayer += 1
        if functionLayer >= len(execLineNumber):
          execLineNumber.append(line[1])
        else:
          execLineNumber[functionLayer] = line[1]
        if functionLayer >= len(controlState):
          controlState.append(0)
        else:
          controlState[functionLayer] = 0
        if functionLayer >= len(indentation):
          indentation.append(1)
        else:
          indentation[functionLayer] = 1
        if functionLayer >= len(switchVariable):
          switchVariable.append(None)
        else:
          switchVariable[functionLayer] = None
        continue
  
      elif line[0] in ["endfunc", "return"]:
        functionLayer -= 1
  
      elif line[0] in ["quit", "end"]:
        exit()
  
    elif controlState[functionLayer] == 1:
      if line[0] == "elseif" and line[-1] == indentation[functionLayer]:
        if getBoolValue(line[1]):
          controlState[functionLayer] = 0
  
      elif line[0] == "else" and line[-1] == indentation[functionLayer]:
        controlState[functionLayer] = 0
  
      elif line[0] == "endcond" and line[-1] == indentation[functionLayer]:
        controlState[functionLayer] = 0
        indentation[functionLayer] -= 1
  
    elif controlState[functionLayer] == 2:
      if line[0] == "case" and line[-1] == indentation[functionLayer]:
        if getValue(line[1]) == switchVariable[functionLayer]:
          controlState[functionLayer] = 0
  
      elif line[0] == "else" and line[-1] == indentation[functionLayer]:
        controlState[functionLayer] = 0
  
    elif controlState[functionLayer] == 3:
      if line[0] == "endcond" and line[-1] == indentation[functionLayer]:
        controlState[functionLayer] = 0
        indentation[functionLayer] -= 1
  
    elif controlState[functionLayer] == 4:
      if line[0] == "while" and line[-1] == indentation[functionLayer] + 1:
        if getBoolValue(line[1]):
          controlState[functionLayer] = 0
        else:
          controlState[functionLayer] = 5
        indentation[functionLayer] += 1
  
      elif line[0] == "for" and line[-1] == indentation[functionLayer] + 1:
        vars[int(line[1][2:])] += getNumberValue(line[4]) #not first time
        if line[1][1] == "i": vars[int(line[1][2:])] = int(vars[int(line[1][2:])])
        if (getNumberValue(line[4]) >= 0 and vars[int(line[1][2:])] <= getNumberValue(line[3])) or (getNumberValue(line[4]) < 0 and vars[int(line[1][2:])] >= getNumberValue(line[3])):
          controlState[functionLayer] = 0
        else:
          controlState[functionLayer] = 5
        indentation[functionLayer] += 1
  
      elif line[0] == "endloop" and line[-1] == indentation[functionLayer]:
        execLineNumber[functionLayer] = line[1] #jump back to start of loop
        indentation[functionLayer] -= 1
        continue
  
    elif controlState[functionLayer] == 5 and line[0] == "endloop" and line[-1] == indentation[functionLayer]:
        controlState[functionLayer] = 0 #end loop
        indentation[functionLayer] -= 1
        continue
    
    execLineNumber[functionLayer] += 1
