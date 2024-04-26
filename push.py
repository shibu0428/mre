import os
from datetime import datetime

# Commit comment
print("koko")
now = datetime.now()
comment = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
#comment = input("コメント入力")
# Push
os.system('git add .')
os.system('git commit -m {}'.format(comment))
os.system('git push')