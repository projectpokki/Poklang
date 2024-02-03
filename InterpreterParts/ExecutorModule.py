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
