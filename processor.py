#!/usr/bin/python3
import os
import sys
import operator


from modules import logger
import config
 


class Process:

    def __init__(self):
        logger.dump('Processor v1', 'debug')


    #
    # Process file line by line
    #
    def run(self):

        d = {}
        try:
            with open(config.c['log_file'], 'r') as r:
                for line in r:
                    line = line.replace('\r', '')
                    line = line.replace('\n', '')
                    line = line.replace('\t', '')

                    is_line_valid = True

                    if line.find(' /') == -1:
                        is_line_valid = False
                    
                    if line.endswith('HTTP/1.1') == False:
                        is_line_valid = False

                    if is_line_valid == True:
                        try:
                            line = line.split(' HTTP/1.1')[0]
                            method = line.split(' ')[0]
                            line = line.split(method + ' ')[1]

                            line = line.strip()
                            line = line.strip(' ')
                            line = line.strip()

                            if len(line) > 4:
                                try:
                                    d[line] += 1
                                except:
                                    d[line] = 1
                        except:
                            pass
        except:
            print(sys.exc_info())

        # save to out file
        outfile = open(config.c['report_file'], 'a')
        for name in d.keys():
            outfile.write('%s\t%s\r\n' %(name, d[name]))
        outfile.flush()
        outfile.close()

        # delete log file
        outfile = open(config.c['log_file'], 'w')
        outfile.write('')
        outfile.flush()
        outfile.close()

        # sort report file for duplicates
        a = {}
        with open(config.c['report_file'], 'r') as r:
            for line in r:
                line = line.replace('\r', '')
                line = line.replace('\n', '')
                tmp = line.split('\t')

                if len(tmp) < 2:
                    continue

                name = tmp[0]
                freq = tmp[1]
                freq = int(freq)
                
                try:
                    a[name] += freq
                except:
                    a[name] = freq

        sorted_x = sorted(a.items(), key=operator.itemgetter(1), reverse=True)

        # save to out file
        outfile = open(config.c['report_file'], 'w')
        for x in sorted_x:
            outfile.write('%s\t%s\r\n' %(x[0], x[1]))
        outfile.flush()
        outfile.close()




if __name__ == '__main__':
    proc = Process()
    proc.run()