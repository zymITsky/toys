## Virtual Machine 2.3.1
## 小步语义  -- 表达式、语句
## python 3.4
class Number(object):
    """ 数值符号类
    """
    def __init__(self, value):
        self.value = value

    def reducible(self):
        return False

    def to_s(self):
        return str(self.value)


class Boolean(object):
    """ 布尔值符号类型
    """
    def __init__(self, value):
        self.value = value

    def reducible(self):
        return False

    def to_s(self):
        return str(self.value)



class Add(object):
    """ 加法符号类
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible():
            return Add(self.left.reduce(environment), self.right)
        elif self.right.reducible():
            return Add(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value + self.right.value)

    def to_s(self):
        return self.left.to_s() + ' + ' + self.right.to_s()
    

class Multiply(object):
    """ 乘法符号类
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible():
            return Multiply(self.left.reduce(environment), self.right)
        elif self.right.reducible():
            return Multiply(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value * self.right.value)
        
    def to_s(self):
        return self.left.to_s() + ' * ' + self.right.to_s()


class LessThan(object):
    """ 小于符号类
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible():
            return LessThan(self.left.reduce(environment), self.right)
        elif self.right.reducible():
            return LessThan(self.left, self.right.reduce(environment))
        else:
            return Boolean(self.left.value < self.right.value)

    def to_s(self):
        return self.left.to_s() + ' < ' + self.right.to_s()


class Variable(object):
    """ 变量符号类
    """
    def __init__(self, name):
        self.name = name

    def reducible(self):
        return True

    def reduce(self, environment):
        return environment[self.name]

    def to_s(self):
        return str(self.name)
    

class DoNothing(object):
    def to_s(self):
        return 'do-nothing'

    def __eq__(self, other_statement):
        return isinstance(other_statement, DoNothing)

    def reducible(self):
        return False


class Assign(object):
    """ 变量赋值语句的实现
    """
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def to_s(self):
        return '{name} = {exp}'.format(name=self.name, exp=self.expression.to_s())

    def reducible(self):
        return True

    def reduce(self, environment):
        if self.expression.reducible():
            return Assign(self.name, self.expression.reduce(environment)), environment
        else:
            return DoNothing(), dict(environment, **{self.name:self.expression})


class Machine(object):
    """ 虚拟机
    """
    def __init__(self, statement, environment):
        self.statement = statement
        self.environment = environment

    def step(self):
        self.statement, self.environment = self.statement.reduce(self.environment)

    def run(self):
        while self.statement.reducible():
            print(self.statement.to_s(), end=', ')
            print([(k, v.value) for k, v in self.environment.items()])
            self.step()
        print(self.statement.to_s(), end=', ')
        print([(k, v.value) for k, v in self.environment.items()])


##test
##x = 2, x = x + 1, x = 3
Machine(
    Assign('x', Add(Variable('x'), Number(1))),
    {'x': Number(2)}
    ).run()
