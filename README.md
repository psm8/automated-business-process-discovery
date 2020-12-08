# automated-business-process-discovery
 
### Simplicity

### Replay fitness
event_group must have fixed length
needlemann-wunsch recurrent and fill matrix
dont have to check next elements in model
nv('pqrklabcdefz', 'zxyabcdefpqr')
nv('klabc', 'abcde')
nv('labcd', 'abcde')
nv('abcde', 'abcde')check also additional ones and add with +1
check next elements in log until more than -1 penalty (-2, -3 , -4)
if eventParallelGroup we still have to solve this for all combinations
need to throw exception when same processes inside and, opt, xor
for and we can just check all characters with skipping all to adding all 
tak all substrings of string
add method to recurrent parallel calculation to choose on substring that makes sense not take one before smallest [-3, -2, -1 ,0, -1, 0, -1, -2 , -3]
gate should always return list of events
add to loop to_n_length return seq if same gates
test model same event name in gate but inside other gates
imporove and to have ['a', 'b', 'c', and] not calc all combos
### Precision
add info about visited nodes and no of children, could be stored in dictionary created when parsing.
### Generalization
add info about visited nodes and no of children, could be stored in dictionary created when parsing.

merge lop if repetitions

consider if opt should return element length n or 0 to n