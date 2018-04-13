import sys
import os


def main(mapfile):
    with open(mapfile, 'rt') as file:
        lines = file.readlines()
        with open('output.txt', 'w') as file_out:
            file_out.write(str(len(lines))+'\n')
            file_out.write(str(len(lines))+'\n')
            for line in lines:
                file_out.write('0')
                for index, char in enumerate(line):
                    if char == '\t' and line[index-1] == 'F':
                        file_out.write('1')
                    if char == '\t' and line[index-1] == '\t':
                        file_out.write('0')
                file_out.write('0')
                file_out.write('\n')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: <map_parser> <mapfile to parse>")
    else:
        main(sys.argv[1])
