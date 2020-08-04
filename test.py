import textfsm
import os
import xlrd
import pandas as pd
import csv
import xlwt

from openpyxl.workbook import Workbook
from openpyxl.styles import Font, Color, Alignment, Border, Side, colors


wb = Workbook()

def all_func(logfile):

    input_file = open(logfile, encoding='utf-8')
    raw_text_data = input_file.read()
    input_file.close()

    fullname = os.path.basename(logfile)
    fullname = fullname.split(".")[0]

    outfile_name = open("output.csv", "w+")
    outfile = outfile_name

    def parse_func(filename, title, header_flag):
        template = open(filename)
        re_table = textfsm.TextFSM(template)
        fsm_results = re_table.ParseText(raw_text_data)

        if header_flag == "true":
            outfile.write("\n%s\n" % title)
            for s in re_table.header:
                outfile.write("%s," % s)
            outfile.write("\n")

        for row in fsm_results:
            print(row)
            for s in row:
                outfile.write("%s," % s)
            outfile.write("\n")

    parse_func("show_ip_bgp_summary.textfsm", "show ip bgp summary", "true")
    parse_func("show_cdp_neigh.textfsm", "show cdp neigh", "true")
   
    template = open("parse.textfsm")
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(raw_text_data)

    past = ''
    for row in fsm_results:
        if past != row[0]:
            outfile.write('\n')
            outfile.write('show ip bgp neighbors %sroutes' % row[0])
            outfile.write('\n')
            for s in re_table.header:
                if s == re_table.header[0]:
                    continue
                outfile.write("%s," % s)
            outfile.write("\n")        
            past = row[0]
        for s in row:
            if s == row[0]:
                continue
            outfile.write("%s," % s)
        outfile.write('\n')

    
    
    parse_func("show_ip_route_vrf_OM.textfsm", "show ip route vrf OM", "true")
    parse_func("show_ip_route_vrf_OM3.textfsm", "show ip route vrf OM", "false")
    parse_func("show_ip_route_vrf_OM1.textfsm", "show ip route vrf OM", "false")
    parse_func("show_ip_route_vrf_OM2.textfsm", "show ip route vrf OM", "false")

    outfile.close()
    
    ws1 = wb.create_sheet(str(fullname), 0)
    with open('output.csv', 'r') as f:
        for row in csv.reader(f):
            ws1.append(row)
                
    wb.save('name.xlsx')

arr_txt = [x for x in os.listdir() if x.endswith(".log") or x.endswith(".txt")]

for file_name in arr_txt:
    all_func(file_name)