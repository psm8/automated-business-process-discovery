# automated-business-process-discovery
 
 
### Gate returns:
    gate -> [BaseGroup] - parallel
    local_list -> [[BaseGroup], [BaseGroup], ...] - parallel
    global_list -> [[[BaseGroup], [BaseGroup], ...], [[BaseGroup], [BaseGroup], ...], ...] - linear
    
    Add lop max length - done
    Gate max size expecially opt - done
    Check with process list - done
    Check with result
    Consider adding unique to list
    to_n_length is too slow - add exception when lop have too many children - done
    add stop when calc n+i if result better than -i
    don't unneceserly wrap single  events in groups
    consider hash recognize eventGroup inside eventGroup
    also maybe checking in constructor if event group added to eventgroup 
    caching shold be done class higher possibly
    return None instead of empty list if empty imposible always chec with min length becaouse gate could have optinal inside
### Simplicity

### Replay fitness
    event_group must have fixed length - done
    needlemann-wunsch recurrent and fill matrix - done
dont have to check next elements in model
check next elements in log until more than -1 penalty (-2, -3 , -4)
if eventParallelGroup we still have to solve this for all combinations
    need to throw exception when same processes inside and, opt, xor - done
take all substrings of string
add method to recurrent parallel calculation to choose on substring that makes sense not take one before smallest [-3, -2, -1 ,0, -1, 0, -1, -2 , -3]
gate should always return list of events
add to loop to_n_length return seq if same gates
test model same event name in gate but inside other gates
improve and to have ['a', 'b', 'c', and] not calc all combos
### Precision
add info about visited nodes and no of children, could be stored in dictionary created when parsing.
### Generalization
add info about visited nodes and no of children, could be stored in dictionary created when parsing.

merge lop if repetitions

consider if opt should return element length n or 0 to n