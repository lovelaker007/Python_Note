#coding:utf-8  

try:
    import cPickle as pickle
except:
    import pickle


data_list = [[1, 1, 'yes'],  
            [1, 1, 'yes'],  
            [1, 0, 'no'],  
            [0, 1, 'no'],  
            [0, 1, 'no']]  

data_dict = { 0: [1, 2, 3, 4],  
            1: ('a', 'b'),  
            2: {'c':'yes','d':'no'}}  


# pickle序列化自定义类
class MyClass():

    def __init__(self, path):
        # 常规属性
        self.path = path
        # 指向下一个MyClass类型的对向
        self._next = None
        # 文件描述符，不能被pickle
        self.fd = None

    def __getstate__(self):
        state = self.__dict__.copy()
        # 对于不能序列化的fd，在序列化时，需要手动删除
        del state['fd']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # 手动添加fd
        self.fd = open(self.path, 'r')
        return state

  
def dump_inner_object():
    # fw = open('pickle_file','wb')  
    with open('pickle_file', 'wb') as f:
        # Pickle the list using the highest protocol available.  
        pickle.dump(data_list, f, -1)  
        # Pickle dictionary using protocol 0.  
        pickle.dump(data_dict, f)  
        # fw.close()  

def load_inner_object():
    # fr = open('pickle_file','rb')  
    with open('pickle_file', 'rb') as f:
        data1 = pickle.load(f)  
        print(data1)  
        data2 = pickle.load(f)  
        print(data2)  

def dump_myclass():
    m1 = MyClass('try_os.py')
    m2 = MyClass('try_iter.py')
    m1._next = m2
    # 在序列化m1时，会自动检查他的下一个对象
    with open('pickle_file', 'wb') as f:
        pickle.dump(m1, f)  

def load_myclass():
    with open('pickle_file', 'rb') as f:
        m1 = pickle.load(f)  
        print(m1.fd)  
        print(m1._next.fd)
 

if __name__ == '__main__':
    # dump_inner_object()
    # load_inner_object()
    dump_myclass()
    load_myclass()
