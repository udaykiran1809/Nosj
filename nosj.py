#!/usr/bin/env python3

import sys
import urllib.parse as parse_url

def map_parser(map):
    try:
        global print_con
        key = []
        key_1 = False
        value = []
        inner_map = False
        inner_list = []
        inner_key = []
        list_temp = []
        temp = []
        temp_value = []
        outter = False
        for i in range(0,len(map)):
            if map[i] == ':' and map[i+1] == '{':
                inner_map = True
                key.append(map[i-1])
                inner_list = []
                list_temp = []

            elif inner_map and map[i] == '}':
                inner_map = False
                str_2 = ''.join(inner_list)
                list_temp.append(str_2)
                value.append(list_temp)
                inner_key = []
                inner_list = []
            elif not inner_map:
                if map[i] == ':':
                    key.append(map[i-1])
                    outter = True
                else:
                    if outter:
                        if map[i] !=',' and map[i] !='}' and map[i] !='{':
                            temp_value.append(map[i])
                        else:
                            str_2 = ''.join(temp_value)
                            value.append(str_2)
                            temp_value = []
                            outter = False
            elif inner_map:
                if map[i] == '{':
                    pass
                else:
                    inner_list.append(map[i])
        
    
        for i in range(0,len(key)):
            if i == 0:
                print_con += 'begin-map\n'
            if isinstance(value[i], list):
                print_con +=f'{key[i]} -- map -- \n'
                print_con += 'begin-map\n'
                inner_solve(value[i])
                print_con+='end-map\n'
            else:
                temp_, type_ = value_(value[i])
                print_con += ("{key} -- {type_} -- {value}\n".format(key = key[i], type_ = type_, value=temp_))

    except:
        pass

def value_(v):
    l = len(v)
    if v[0] == 'f' and v[l-1] == 'f' and l>1:
        num = float(v.split('f')[1].split('f')[0])
        if num.is_integer():
            num = int(num)
        return num, 'num' 
    
    elif v[l-1] == 's':
        string =  str(v.split('s')[0])
        return string, 'string'
    elif '%' in v:
        string = parse_url.unquote(v)
        return string, 'string'


def inner_solve(v):
    global print_con
    i = v[0]
    count = 0
    if ',' in i:
        temp = i.split(',')
        for j in temp:
            count = count+1
            temp_2 = j.split(':')
            temp_,type_ = value_(temp_2[1])
            print_con += ("{key} -- {type_} -- {value}\n".format(key = temp_2[0], type_ = type_, value=temp_))

    else:
        count = count+1
        temp = i.split(':')
        temp_, type_ = value_(temp[1])
        print_con += ("{key} -- {type_} -- {value}\n".format(key = temp[0], type_ = type_, value=temp_))

def print_err(err_mesg):
    sys.stderr.write("ERROR -- {mesg}\n".format(mesg = err_mesg))
    sys.exit(66)

if __name__ == '__main__':
    try:
        count = 0
        count_1 = 0
        read_file = open(sys.argv[1], 'r')
        data = read_file.read()
        data = data.split("\n")[0]
        data = data.rstrip(" ")
        data = data.lstrip(" ")
        print_con = ''
        if data.startswith("<<") and data.endswith(">>"):
            data = data.replace('<<','{')
            data = data.replace('>>','}')
            for i in data:
                if i == '{':
                    count = count +1
                elif i == '}':
                    count_1 = count_1+1
            
            if count == count_1:
                for i in range(0,len(data)):
                    if data[i] == " ":
                        if data[i-1] == "{":
                            print_err("Invalid Map")
                    elif i == len(data)-1:
                        if data[i-1] == ' ':
                            print_err("Invalid Map")
                    elif data[i] == ':':
                        if data[i-1] == ' ' or data[i+1] == ' ':
                            print_err("Invalid Map")                            

                map_parser(data)
                print_con +='end-map'
                print(print_con)
            else:
                print_err("Invalid Map")
        else:
            print_err("Invalid Map")
    
    except Exception as e:
        print_err(str(e))
