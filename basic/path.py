# 获取图书的存储路径:
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 存书
FILE_PATH1 = os.path.join(BASE_DIR, 'DB', 'book_base.csv')

# 借书
FILE_PATH2 = os.path.join(BASE_DIR, 'DB', 'borrow_base.csv')




