# ファイル名をハッシュ化するコード
# https://freeheroblog.com/filename-hash/

import os
import hashlib
from datetime import datetime


def _user_profile_avator_upload_to(filename):
    current_time = datetime.now()
    pre_hash_name = '%s%s' % (filename, current_time)
    extension = str(filename).split('.')[-1]
    hs_filename = '%s.%s' % (hashlib.md5(pre_hash_name.encode()).hexdigest(), extension)
    saved_path = 'media/'
    return '%s%s' % (saved_path, hs_filename)


filename = "エンジニアカタパルト.png"
# extension = str(filename).split('.')[-1]
# hs_filename = '%s.%s' % (hashlib.md5(file_name.encode()).hexdigest(), extension)
# print(hs_filename) #364be8860e8d72b4358b5e88099a935a.png

print(_user_profile_avator_upload_to(filename))
