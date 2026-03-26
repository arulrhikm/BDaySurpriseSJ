import re

path = r'c:\Users\arulr\Projects\BDayLetter\index.html'
content = open(path, 'r', encoding='utf-8').read()

# Change Rue's object-fit to contain so the whole cat is visible in the circle
old = 'object-position: 85% 5%'
new = 'object-position: center; object-fit: contain'
content = content.replace(old, new)

open(path, 'w', encoding='utf-8').write(content)
print('Fixed Rue alignment to object-fit: contain')
