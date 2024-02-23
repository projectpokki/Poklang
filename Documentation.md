TOKENS:

end           - ends program

var a         - define variable a
set a b       - a = b

say a b c...  - print(a, b, c...)
input a       - a = input()

add c a b     - c = a + b (nums only)
sub c a b     - c = a - b (nums only)
mul c a b     - c = a * b (nums only)
div c a b     - c = a / b (nums only)
mod c a b     - c = a % b (nums only)

abs c a       - c = abs(a) (nums only)
sqrt c a      - c = sqrt(a) (nums only)
flr c a       - c = floor(a), always rounds down (nums only)

conc c a b     - c = a + b (strs only)
cut c a b d   - c = b[a:b] (strs only)
char c a b     - c = b[a] (strs only)
len c a       - c = len(a) (strs only)

equ c a b     - c is true if a == b
dif c a b     - c is true if a != b, also functions as [XOR gate]
grt c a b     - c is true if a > b (nums only)
grteq c a b   - c is true if a >= b (nums only)

not a b       - a is true if b is false (bools only)
and c a b     - c is true if a and b are both true (bools only)
or c a b      - c is true if either a or b are true (bools only)

if a b        - if a then continue, else jump downwards by b lines
goto a        - go to line a
for a b c d.    - for loop, goes at the end of loop. use goto to skip first iteration. for a = b, a < c, (a += d), length of loop

ston a b.     - string to num, a is output, b is input
ntos a b.     - num to string, a is output, b is input
ctob a b.     - char to ascii value (int), a is output, b is input
btoc a b.     - ascii value (int) to char, a is output, b is input

CONSTANTS:

str a b c     - b is constant string. a is how many words long it is. c is a constant string (cannot contain spc or nl, only achieveable by concatenation)
num a         - a is constant floating point value
bool a        - a is either yes (true) or no (false)
spc           - space character (" ")
nl            - \n

(FOR DEBUG) INTERPRETER ACTION ENUMS:
-1 - end
0 - var
1 - set
2 - say
3 - input
4 - add
5 - sub
6 - mul
7 - div
8 - mod
9 - abs
10 - exp
11 - flr
12 - conc
13 - cut
14 - char
15 - len
16 - equ
17 - dif
18 - grt
19 - grteq
20 - not
21 - and
22 - or
23 - goto
24 - if
25 - for
26 - ston
27 - ntos
28 - ctob
29 - btoc
