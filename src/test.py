import re
str1 = "<rect(513, 484, 282, 104)>"
print(re.findall(r'\d+',str1))