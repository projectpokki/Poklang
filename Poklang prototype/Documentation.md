TOKENS:

end           - ends program

var a         - define variable a<br>
set a b       - a = b

say a b c...  - print(a, b, c...)<br>
input a       - a = input()

add c a b     - c = a + b (nums only)<br>
sub c a b     - c = a - b (nums only)<br>
mul c a b     - c = a * b (nums only)<br>
div c a b     - c = a / b (nums only)<br>
mod c a b     - c = a % b (nums only)

abs c a       - c = abs(a) (nums only)<br>
sqrt c a      - c = sqrt(a) (nums only)<br>
flr c a       - c = floor(a), always rounds down (nums only)<br>

conc c a b     - c = a + b (strs only)<br>
cut c a b d   - c = b[a:b] (strs only)<br>
char c a b     - c = b[a] (strs only)<br>
len c a       - c = len(a) (strs only)<br>

equ c a b     - c is true if a == b<br>
dif c a b     - c is true if a != b, also functions as [XOR gate]<br>
grt c a b     - c is true if a > b (nums only)<br>
grteq c a b   - c is true if a >= b (nums only

not a b       - a is true if b is false (bools only)<br>
and c a b     - c is true if a and b are both true (bools only)<br>
or c a b      - c is true if either a or b are true (bools only)

if a b        - if a then continue, else jump downwards by b lines<br>
goto a        - go to line a<br>
for a b c d.    - for loop, goes at the end of loop. use goto to skip first iteration. for a = b, a < c, (a += d), length of loop

ston a b.     - string to num, a is output, b is input<br>
ntos a b.     - num to string, a is output, b is input<br>
ctob a b.     - char to ascii value (int), a is output, b is input<br>
btoc a b.     - ascii value (int) to char, a is output, b is input

CONSTANTS:

str a b c     - b is constant string. a is how many words long it is. c is a constant string (cannot contain spc or nl, only achieveable by concatenation)<br>
num a         - a is constant floating point value<br>
bool a        - a is either yes (true) or no (false)<br>
spc           - space character (" ")<br>
nl            - \n

(FOR DEBUG) INTERPRETER ACTION ENUMS:<br>
-1 - end<br>
0 - var<br>
1 - set<br>
2 - say<br>
3 - input<br>
4 - add<br>
5 - sub<br>
6 - mul<br>
7 - div<br>
8 - mod<br>
9 - abs<br>
10 - exp<br>
11 - flr<br>
12 - conc<br>
13 - cut<br>
14 - char<br>
15 - len<br>
16 - equ<br>
17 - dif<br>
18 - grt<br>
19 - grteq<br>
20 - not<br>
21 - and<br>
22 - or<br>
23 - goto<br>
24 - if<br>
25 - for<br>
26 - ston<br>
27 - ntos<br>
28 - ctob<br>
29 - btoc
