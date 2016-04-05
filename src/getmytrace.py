#!/usr/bin/env python

'''
Owner:      SHI, Chen
E-mail:     chen.shi@alcatel-lucent.com

History:
            v0.1    2016-03-17    SHI, Chen    init version
            v0-2    2016-04-05    SHI, Chen    [fea001] support getting RTDB insert trace 

'''

import sys
import re

# define the pattern for my traces
my_trace_pattern_list = [
                         'TRACE:\s+diameter!credit_control_request_received',
                         'TRACE:.*_RTDB!read\(',
                         'TRACE:.*_RTDB!insert\(',
                         'TRACE:.*_RTDB!delete\(',
                         'TRACE:.*_RTDB!update\(',
                         'TRACE:.*_RTDB!search\(',
                         'TRACE:.*\(Al',
                         ]
my_trace_list = []

def get_all_my_trace(debuglog):
    '''analyze the debuglog and get all my traces into my_trace_list.'''
    
    num = 0
    while num < len(debuglog):
        
        # loop the pattern list
        for pattern in my_trace_pattern_list:
            #print 'current pattern is', pattern

            # analyze debuglog            
            match_result = re.search(pattern, debuglog[num])
            if match_result:
                #my_trace_list.append(match_result.group(0))
                my_trace_list.append(debuglog[num])
        
        # increase line number
        num += 1

    return


def analyze_my_trace_for_rtdb_actions():
    '''analyze my trace for RTDB actions'''
    
    my_rtdb_action_dict = {}
    ccrnum = 0
    
    for line in my_trace_list:
        
        # analyze CCR trace
        match_result = re.search(r'TRACE:\s+diameter!credit_control_request_received', line)
        if match_result:
            # CCR +1
            ccrnum += 1
            continue
        
        # analyze RTDB trace
        match_result = re.search(r'TRACE:.*\s(\S+_RTDB!\S+)\(ins', line)
        if match_result:
            my_key = 'CCR%s:%s' % (str(ccrnum).zfill(2), match_result.group(1)) 

            # RTDB Action +1            
            if my_rtdb_action_dict.has_key(my_key):
                my_rtdb_action_dict[my_key] += 1
            else:
                my_rtdb_action_dict[my_key] = 1

    # dump the result
    for my_key in sorted(my_rtdb_action_dict.keys()):
        print my_key, '\t', my_rtdb_action_dict[my_key]
    
    
def print_all_my_trace():
    '''print all my traces'''
    for line in my_trace_list:
        print line,

    return


def main():
    '''get traces from specified debuglog.'''
    
    if len(sys.argv) < 2:
        print 'Usage: calcmeas.py <debuglog file>'
        return
    else:
        print "Debuglog file: ", sys.argv[1]
        
        # read file
        f = open(sys.argv[1], 'r')
        debuglog = f.readlines()
        f.close()

    get_all_my_trace(debuglog)
    
    print '=' * 60
    print_all_my_trace()
    print '=' * 60
    analyze_my_trace_for_rtdb_actions()
    print '=' * 60
    print 'finished!'
    
    return


if __name__ == '__main__':
    main()
