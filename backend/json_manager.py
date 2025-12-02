'''提供JsonManager类，实现json文件的初始化和基本的结构创建，读写操作'''

import json
import pickle
import gzip

def test_form(file_path:str)->str:
    '''用于检索文件类型'''
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            print("✅ 用 JSON 读取成功！")
            return 'utf-8'
    except UnicodeDecodeError:
        print("❌ 不是 UTF-8 编码的文本文件，尝试二进制格式...")

        # 尝试用 pickle 读取
        try:
            with open(file_path, 'rb') as f:
                print("✅ 用 Pickle 读取成功！")
            return 'rb'
        except Exception as e:
            print(f"❌ 不是 Pickle 文件: {e}")

            try:
                with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                    print("✅ 用 Gzip + JSON 读取成功！")
                return 'g'
            except Exception as e:
                print(f"❌ 不是 Gzip 文件: {e}")
                raise


def open_fuc(form,file_path):
    '''读取文件'''
    if form=='utf-8':
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif form=='rb':
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    elif form=='g':
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            return json.load(f)
    else:
        print('='*50)
        print('FormError')
        raise ValueError("无法识别文件格式")
    


import json
import os

class JsonManager:
    """JSON文件管理器
    
    用于管理JSON格式的数据文件，提供基本的读写操作。
    注意：修改数据后需要手动调用save_json()保存。
    
    Args:
        file_path (str): JSON文件的位置路径
        stru: JSON文件的结构模板
    
    Example:
        >>> # 创建用户数据管理器
        >>> jm = JsonManager("users.json", {"users": [], "count": 0})
        >>> jm.data["users"].append({"name": "Alice", "age": 25})
        >>> jm.save_json()  # 必须手动保存
    """
    def __init__(self,file_path,stru = None):
        self.file_path=file_path
        self.stru=stru
        self.data=self._load_json()
        
    def _load_json(self):
        if os.path.exists(self.file_path):
            return open_fuc(test_form(self.file_path),self.file_path)
        else:
            return self._create_json()

    def _create_json(self):
        '''创建初始json文件的结构'''
        return self.stru
    
    def save_json(self) -> bool:
        """将数据保存到json文件中"""
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
                print(f'保存成功到{self.file_path}')
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False
        
    def remove_json(self) -> bool:
        '''永久删除json文件'''
        try:
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
                return True
            return False
        except Exception as e:
            raise e

