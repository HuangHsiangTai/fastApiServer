import random
import string

def generate_uuid(length=10):
    # 使用字母和数字生成随机的唯一标识符
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))