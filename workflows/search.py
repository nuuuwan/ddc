import sys
from ddc import Raw

root = Raw().parse()

print('🔎Running DDC search...')

search_phrase = sys.argv[1]
root.search(search_phrase)

print('▪️')
