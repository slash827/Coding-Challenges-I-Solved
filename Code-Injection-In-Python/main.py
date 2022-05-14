# I used the file injected_file.py to check my code and the code below works
# for all files accept for the part of executing the
# methods, in which I tested specifically those of my file


class Replicator:
    def deco(self, f, code):
        def ret(*args):
            exec(code)
            f(*args)
        return ret

    def affect(self, obj, code):
        # here we make sure that the method is not a magic method
        cls = obj.__class__
        for attr, item in cls.__dict__.items():
            if callable(item) and attr[:2] != '__' and attr[-2:] != '__':
                setattr(cls, attr, self.deco(item, code))


def main():
    # first we take the file name as input
    file_name = input("please enter the name of the file:\n")
    # file_name = 'example_for_meta'

    # then we take the class name as input
    class_name = input("please enter the class name:\n")
    # class_name = 'A'

    # then we take the code itself as input
    code = input("hello please enter a line of code:\n")
    # code = 'print("hello")'

    # here we make the custom importing of that file
    import_statement = 'from ' + file_name + ' import ' + class_name + ' as E'
    # executes the line: from example_for_meta import A as E
    exec(import_statement)

    # here we declare the object and inject code to it
    # equals to the line: obj = E()
    obj = eval('E()')
    r = Replicator()
    r.affect(obj, code)

    # all methods will run here to verify
    obj.increase1()
    obj.decrease1()


if __name__ == '__main__':
    main()
