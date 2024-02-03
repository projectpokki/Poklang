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
