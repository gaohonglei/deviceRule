# coding: UTF-8

'''''
ty 参数用于按序判断参数类型是否正确，argv参数用于判断具体某一参数类型是否正确
example：ParamCheck(int,int,x=str)

'''


def ParamCheck(*ty, **argv):
    ty = map(ToCheckFun, ty)
    argv = dict((i, ToCheckFun(argv[i])) for i in argv)

    def common(fun):
        def deal(*fun_x, **fun_y):
            if ty:
                x_list = [a for a in fun_x]
                x_list_it = iter(x_list)
                result = []
                for t_check in ty:
                    r = t_check(x_list_it.next())
                    result.append(r)

                print 'param check result: ', result

            if argv:
                y_dic = dict((i, fun_y[i]) for i in fun_y)
                result = {}
                for k in argv.keys():
                    f = argv[k](y_dic.get(k))
                    result[k] = f
                print 'param check result: ', result

            return fun(*fun_x, **fun_y)

        return deal

    return common


# 用于生成判断具体参数的函数
def ToCheckFun(t):
    return lambda x: isinstance(x, t)


@ParamCheck(int, str, c=int)
def fun_1(a, b, c):
    pass
@ParamCheck(int,str,c=int)

def unit_test():
    fun_1(1, 2, c='ss')


if __name__ == '__main__':
    unit_test()