fileName = "Poklang.txt" #set this variable to the name of the Poklang file you are running.

def tokenize(file):
  rawCode = open(file, "r", encoding="utf-8")
  tokens = []
  while True:
    rawLine = rawCode.readline()
    if rawLine == "":
      return tokens
    if rawLine[0] == "\n" or rawLine[0] == "-":
      tokens.append([-2])
      continue
    tokens.append(rawLine.split())

def makeStr(line, start, length):
  string = "s"
  for i in line[start:(length + start)]:
    string += str(i) + " "
  return string[:-1]

def parse(tokens):
  vars = {}
  for line in tokens:
    if line[0] == -1: line[0] = None
    elif line[0] == "end": line[0] = -1

    elif line[0] == "var":
      line[0] = 0
      vars[line[1]] = "v" + str(len(vars))
      line[1] = vars[line[1]]

    elif line[0] == "set":
      line[0] = 1
      line[1] = vars[line[1]]
      if line[2] == "num": line[2] = float(line[3])
      elif line[2] == "str": line[2] = makeStr(line, 4, int(line[3]))
      elif line[2] == "bool" and line[3] == "true": line[2] = True
      elif line[2] == "bool" and line[3] == "false": line[2] = False
      elif line[2] == "spc": line[2] = "s "
      elif line[2] == "nl": line[2] = "s\n"
      else: line[2] = vars[line[2]]
      line = line[:3]

    elif line[0] == "say":
      line[0] = 2
      i = 1
      for word in range(1, len(line)):
        if word < i:
          line[word] = "s"
          continue
        elif line[word] in vars:
          line[word] = vars[line[word]]
        elif line[word] == "num":
          line[word] = float(line[word + 1])
          i += 1
        elif line[word] == "str":
          line[word] = makeStr(line, word + 2, int(line[word + 1]))
          i += int(line[word + 1]) + 1
        elif line[word] == "spc":
          line[word] = "s "
        elif line[word] == "nl":
          line[word] = "s\n"
        i += 1

    elif line[0] == "input":
      line[0] = 3
      line[1] = vars[line[1]]

    elif line[0] in {"add", "sub", "mul", "div", "mod", "exp", "grt", "grteq"}:
      if line[0] == "add": line[0] = 4
      elif line[0] == "sub": line[0] = 5
      elif line[0] == "mul": line[0] = 6
      elif line[0] == "div": line[0] = 7
      elif line[0] == "mod": line[0] = 8
      elif line[0] == "exp": line[0] = 10
      elif line[0] == "grt": line[0] = 18
      elif line[0] == "grteq": line[0] = 19

      line[1] = vars[line[1]]
      if line[2] == "num":
        line[2] = float(line[3])
        if line[4] == "num": line[3] = float(line[5])
        else: line[3] = vars[line[4]]
      else:
        line[2] = vars[line[2]]
        if line[3] == "num": line[3] = float(line[4])
        else: line[3] = vars[line[3]]
      line = line[:4]

    elif line[0] in {"abs", "flr"}:
      if line[0] == "abs": line[0] = 9
      elif line[0] == "flr": line[0] = 11
      line[1] = vars[line[1]]
      if line[2] == "num": line[2] = float(line[3])
      else: line[2] = vars[line[2]]
      line = line[:3]

    elif line[0] == "conc":
      line[0] = 12
      line[1] = vars[line[1]]

      if line[2] == "str":
        line[2] = makeStr(line, 4, int(line[3]))
        if line[4 + int(line[3])] == "str": line[3] = makeStr(line, 6 + int(line[3]), 5 + int(line[3]))
        elif line[4 + int(line[3])] == "spc": line[3] = "s "
        elif line[4 + int(line[3])] == "nl": line[3] = "s\n"
        else: line[3] = vars[line[3]]
      else:
        if line[2] == "spc": line[2] = "s "
        else: line[2] = vars[line[2]]
        if line[3] == "str": line[3] = makeStr(line, 5, int(line[4]))
        elif line[3] == "spc": line[3] = "s "
        elif line[3] == "nl": line[3] = "s\n"
        else: line[3] = vars[line[3]]
      line = line[:4]

    elif line[0] == "cut":
      line[0] = 13
      line[1] = vars[line[1]]
      if line[2] == "num":
        line[2] = int(line[3])
        if line[4] == "num":
          line[3] = int(line[5])
          if line[6] == "str": line[4] = makeStr(line, 8, int(line[7]))
          else: line[4] = vars[line[6]]
        else:
          line[3] = vars[line[4]]
          if line[5] == "str": line[4] = makeStr(line, 7, int(line[6]))
          else: line[4] = vars[line[5]]
      else:
        line[2] = vars[line[2]]
        if line[3] == "num":
          line[3] = int(line[4])
          if line[5] == "str": line[4] = makeStr(line, 7, int(line[6]))
          else: line[4] = vars[line[5]]
        else:
          line[3] = vars[line[3]]
          if line[4] == "str": line[4] = makeStr(line, 6, int(line[5]))
          else: line[4] = vars[line[4]]
      line = line[:5]

    elif line[0] == "char":
      line[0] = 14
      line[1] = vars[line[1]]
      if line[2] == "num":
        line[2] = int(line[3])
        if line[4] == "str": line[3] = makeStr(line, 6, int(line[5]))
        else: line[3] = vars[line[4]]
      else:
        line[2] = vars[line[2]]
        if line[3] == "str": line[3] = makeStr(line, 5, int(line[4]))
        else: line[3] = vars[line[3]]

    elif line[0] == "len":
      line[0] = 15
      line[1] = vars[line[1]]
      if line[2] == "str": line[2] = makeStr(line, 4, int(line[3]))
      else: line[2] = vars[line[2]]

    elif line[0] in {"equ", "dif"}:
      if line[0] == "equ": line[0] = 16
      elif line[0] == "dif": line[0] = 17
      line[1] = vars[line[1]]

      if line[2] == "num":
        line[2] = float(line[3])
        if line[3] == "num": line[3] = float(line[4])
        elif line[3] == "str": line[3] = makeStr(line, 5, int(line[4]))
        elif line[3] == "bool" and line[4] == "true": line[3] = True
        elif line[3] == "bool" and line[4] == "false": line[3] = False
        elif line[3] == "spc": line[3] = "s "
        else: line[3] = vars[line[3]]

      elif line[2] == "str":
        line[2] = makeStr(line, 4, int(line[3]))
        stringEnd = 4 + int(line[3])
        if line[stringEnd] == "num": line[3] = float(line[1 + stringEnd])
        elif line[stringEnd] == "str": line[3] = makeStr(line, 2 + stringEnd, int(line[1 + stringEnd]))
        elif line[stringEnd] == "bool" and line[1 + stringEnd] == "true": line[3] = True
        elif line[stringEnd] == "bool" and line[1 + stringEnd] == "false": line[3] = False
        elif line[stringEnd] == "spc": line[3] = "s "
        else: line[3] = vars[line[3]]

      elif line[2] == "bool":
        if line[3] == "true": line[2] = True
        elif line[3] == "false": line[2] = False

        if line[4] == "num": line[3] = float(line[4])
        elif line[4] == "str": line[3] = makeStr(line, 5, int(line[4]))
        elif line[4] == "bool" and line[5] == "true": line[3] = True
        elif line[4] == "bool" and line[5] == "false": line[3] = False
        elif line[4] == "spc": line[3] = "s "
        else: line[3] = vars[line[3]]

      else:
        if line[2] == "spc": line[2] = "s "
        else: line[2] = vars[line[3]]
        if line[3] == "num": line[3] = float(line[4])
        elif line[3] == "str": line[3] = makeStr(line, 5, int(line[4]))
        elif line[3] == "bool" and line[5] == "true": line[3] = True
        elif line[3] == "bool" and line[5] == "false": line[3] = False
        elif line[3] == "spc": line[3] = "s "
        else: line[3] = vars[line[3]]
      line = line[:4]

    elif line[0] == "not":
      line[0] = 20
      line[1] = vars[line[1]]
      if line[2] == "bool" and line[3] == "true": line[2] = True
      elif line[2] == "bool" and line[3] == "false": line[2] = False
      else: line[2] = vars[line[2]]
      line = line[:3]
      continue

    elif line[0] in {"and", "or"}:
      if line[0] == "and": line[0] = 21
      elif line[0] == "or": line[0] = 22
      line[1] = vars[line[1]]
      if line[2] == "bool":
        if line[3] == "true": line[2] = True
        elif line[3] == "false": line[2] = False
        if line[4] == "bool" and line[5] == "true": line[3] = True
        elif line[4] == "bool" and line[5] == "false": line[3] = False
        else: line[3] = vars[line[4]]
      else:
        line[2] = vars[line[2]]
        if line[3] == "bool" and line[4] == "true": line[3] = True
        elif line[3] == "bool" and line[4] == "false": line[3] = False
        else: line[3] = vars[line[3]]
      line = line[:4]

    elif line[0] == "goto":
      line[0] = 23
      if line[1] == "num": line[1] = int(line[2])
      else: line[1] = vars[line[1]]
      line = line[:2]

    elif line[0] == "if":
      line[0] = 24
      if line[1] == "bool":
        if line[2] == "true": line[1] = True
        elif line[2] == "false": line[1] = False
        if line[3] == "num": line[2] = int(line[4])
        else: line[2] = vars[line[3]]
      else:
        line[1] = vars[line[1]]
        if line[2] == "num": line[2] = int(line[3])
        else: line[2] = vars[line[2]]

    elif line[0] == "for":
      line[0] = 25
      line[1] = vars[line[1]]
      lineWord = 2
      if line[2] == "num":
        line[2] = float(line[3])
        lineWord += 2
      else:
        line[2] = vars[line[2]]
        lineWord += 1
      if line[lineWord] == "num":
        line[3] = float(line[lineWord + 1])
        lineWord += 2
      else:
        line[3] = vars[line[3]]
        lineWord += 1
      if line[lineWord] == "num":
        line[4] = int(line[lineWord + 1])
      else:
        line[4] = vars[line[lineWord]]
      line = line[:5]

    elif line[0] in {"ston", "ctob"}:
      if line[0] == "ston": line[0] = 26
      elif line[0] == "ctob": line[0] = 28
      line[1] = vars[line[1]]
      if line[2] == "str": line[2] = makeStr(line, 4, line[3])
      elif line[2] == "spc": line[2] = "s "
      elif line[2] == "nl": line[2] = "s\n"
      else: line[2] = vars[line[2]]
      line = line[:3]

    elif line[0] in {"ntos", "btoc"}:
      if line[0] == "ntos": line[0] = 27
      elif line[0] == "btoc": line[0] = 29
      line[1] = vars[line[1]]
      if line[2] == "num": line[2] = float(line[3])
      else: line[2] = vars[line[2]]
      line = line[:3]
  return tokens

def varValue(var):
  if type(var) == str:
    if var[0] == "v": return vars[var]
    elif var[0] == "s": return var[1:]
  elif var is True: return True
  elif var is False: return False
  return var

def runCode(tokens):
  global vars
  vars = {}

  lineNumber = 0
  while True:
    line = tokens[lineNumber]
    if line[0] == -1:
      return

    if line[0] is None:
      continue

    elif line[0] == 0:
      vars[line[1]] = None

    elif line[0] == 1:
      vars[line[1]] = varValue(line[2])

    elif line[0] == 2:
      lineOfText = ""
      for i in line[1:]:
        lineOfText += str(varValue(i))
      print(lineOfText)

    elif line[0] == 3:
      vars[line[1]] = input()

    elif line[0] == 4:
      vars[line[1]] = float(varValue(line[2])) + float(varValue(line[3]))

    elif line[0] == 5:
      vars[line[1]] = float(varValue(line[2])) - float(varValue(line[3]))

    elif line[0] == 6:
      vars[line[1]] = float(varValue(line[2])) * float(varValue(line[3]))

    elif line[0] == 7:
      vars[line[1]] = float(varValue(line[2])) / float(varValue(line[3]))

    elif line[0] == 8:
      vars[line[1]] = float(varValue(line[2])) % float(varValue(line[3]))

    elif line[0] == 9:
      vars[line[1]] = abs(float(varValue(line[2])))

    elif line[0] == 10:
      vars[line[1]] = float(varValue(line[2]))**float(varValue(line[3]))

    elif line[0] == 11:
      vars[line[1]] = float(varValue(line[2])) // 1

    elif line[0] == 12:
      vars[line[1]] = str(varValue(line[2])) + str(varValue(line[3]))

    elif line[0] == 13:
      vars[line[1]] = str(varValue(
          line[4]))[int(varValue(line[2])):int(varValue(line[3]))]

    elif line[0] == 14:
      vars[line[1]] = str(varValue(line[3]))[int(varValue(line[2]))]

    elif line[0] == 15:
      vars[line[1]] = len(str(varValue(line[2])))

    elif line[0] == 16:
      if varValue(line[2]) == varValue(line[3]): vars[line[1]] = True
      else: vars[line[1]] = False

    elif line[0] == 17:
      if varValue(line[2]) != varValue(line[3]): vars[line[1]] = True
      else: vars[line[1]] = False

    elif line[0] == 18:
      if float(varValue(line[2])) > float(varValue(line[3])):
        vars[line[1]] = True
      else:
        vars[line[1]] = False

    elif line[0] == 19:
      if float(varValue(line[2])) >= float(varValue(line[3])):
        vars[line[1]] = True
      else:
        vars[line[1]] = False

    elif line[0] == 20:
      if varValue(line[2]): vars[line[1]] = False
      else: vars[line[1]] = True

    elif line[0] == 21:
      if varValue(line[2]) and varValue(line[3]): vars[line[1]] = True
      else: vars[line[1]] = False

    elif line[0] == 22:
      if varValue(line[2]) or varValue(line[3]): vars[line[1]] = True
      else: vars[line[1]] = False

    elif line[0] == 23:
      lineNumber = int(varValue(line[1])) - 1
      continue

    elif line[0] == 24 and varValue(line[1]) is False:
      lineNumber += int(varValue(line[2])) + 1
      continue

    elif line[0] == 25:
      vars[line[1]] += float(varValue(line[3]))
      if float(varValue(line[1])) < float(varValue(line[2])):
        lineNumber -= int(varValue(line[4]))
        continue

    elif line[0] == 26:
      vars[line[1]] = float(varValue(line[2]))

    elif line[0] == 27:
      vars[line[1]] = str(varValue(line[2]))

    elif line[0] == 28:
      vars[line[1]] = ord(str(varValue(line[2])))

    elif line[0] == 29:
      vars[line[1]] = chr(int(varValue(line[2])))

    lineNumber += 1

runCode(parse(tokenize(fileName)))