import sys, datetime
from typing import Sequence

str2datetime = lambda date: datetime.datetime.strptime(date, '%Y%m%d%H%M%S')
ap_add = lambda dat, add, res: {"address": add,
                                "updated_time": [str2datetime(dat)],
                                "response": [int(res)],
                                "cnt_fail": 0
                                }

def check_failure(ad: 'dict', now_time: 'datetime') -> int:
    if response == "-":
        return ad['cnt_fail'] + 1
    else:
        ad['updated_time'].append(now_time)
        ad['response'].append(int(response))
        if ad['cnt_fail'] >= N:
            print(f'failure of {ad["address"]}：　{now_time - ad["updated_time"][-2]}')
        
        return 0

def check_overload(ad: 'dict') -> None:
    len_res = len(ad['response'])
    if len_res > m:
        len_res = m
        _, _ = ad['updated_time'].pop(0), ad['response'].pop(0)
        
    mean = sum(ad['response'])/len_res
    if mean >= t:
        o_value = list(filter(lambda x: x>=t, ad['response']))[-1]
        o_key = ad["response"].index(o_value)
        print(f'{ad["address"]} is overload since：{ad["updated_time"][o_key]}')

if __name__ == '__main__':
  N, m, t = map(int, sys.argv[1:])

  with open("log.txt", mode='r') as f:
    log_file = [ s.strip() for s in f.readlines()]
  # for log in log_file: print(log)

  l_dic = list()
  address_name = list()
  cnt_fail_subnet = 0
  for log in log_file:
    date, address, response = log.split(',')
    # print(date, address, response)
    if not address in address_name:
      if response == '-':
        cnt_fail_subnet += 1
        continue
      address_name.append(address)
      l_dic.append(ap_add(date, address, response))
    else:
      i = address_name.index(address)
      l_dic[i]['cnt_fail'] = check_failure(l_dic[i], str2datetime(date))
      
      check_overload(l_dic[i])

      cnt_fail_subnet = cnt_fail_subnet + 1 if l_dic[i]['cnt_fail'] else 0
      if cnt_fail_subnet == N:
        print('subnet is failure.')
        for ad in l_dic:
          if ad['cnt_fail']:
            print(f'failure of {ad["address"]}：　{str2datetime(date) - ad["updated_time"][-1]}')
