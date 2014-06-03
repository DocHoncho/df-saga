
import re
w = re.compile(r'^(\d+): ([\w\s]+), "(.*)", (\w+)\s+$')
t = w.search('1: Gor Memrut, "The Pits of Crucifixion", cave\r\n')
print(t)
