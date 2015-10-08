# coding=utf-8

def name2desc(cls, name):
    """
    根据枚举量得到枚举量的描述
    :param cls: 类变量
    :param name: 枚举变量的字符名
    :return: 该变量的描述
    """
    return cls.name_describe_map[name]


def name2value(cls, name):
    """
    根据枚举量得到该枚举量的数值
    :param cls:
    :param name:
    :return:
    """
    return cls.__dict__[name]


def build_enum(class_):
    index = 0
    class_.__dict__["name_describe_map"] = {}
    class_.__dict__["name2desc"] = classmethod(name2desc)
    class_.__dict__["name2value"] = classmethod(name2value)

    if type(class_.enum) is dict:
        for i in class_.enum.items():
            class_.name_describe_map[i[0]] = (index, i[1])
            setattr(class_, i[0], index)
            index += 1
    elif type(class_.enum) is list:
        for i in class_.enum:
            setattr(class_, i[0], index)
            index += 1


class EnumException(Exception):
    """ Base class for all exceptions in this module. """

    def __init__(self, *args, **kwargs):
        if self.__class__ is EnumException:
            raise NotImplementedError(
                "%(class_name)s is an abstract base class" % vars())
        super(EnumException, self).__init__(*args, **kwargs)


class EnumEmptyError(AssertionError, EnumException):
    """ Raised when attempting to create an empty enumeration. """

    def __str__(self):
        return "Enumerations cannot be empty"


class EnumBadKeyError(TypeError, EnumException):
    """ Raised when creating an Enum with non-string keys. """

    def __init__(self, key):
        self.key = key

    def __str__(self):
        return "Enumeration keys must be strings: %(key)r" % vars(self)


class EnumImmutableError(TypeError, EnumException):
    """ Raised when attempting to modify an Enum. """

    def __init__(self, *args):
        self.args = args

    def __str__(self):
        return "Enumeration does not allow modification"


def _comparator(func):
    """ Decorator for EnumValue rich comparison methods. """

    def comparator_wrapper(self, other):
        try:
            assert self.enumtype == other.enumtype
            result = func(self.index, other.index)
        except (AssertionError, AttributeError):
            result = NotImplemented

        return result

    comparator_wrapper.__name__ = func.__name__
    comparator_wrapper.__doc__ = getattr(float, func.__name__).__doc__
    return comparator_wrapper


class EnumValue(object):
    """ A specific value of an enumerated type. """

    def __init__(self, enumtype, index, key):
        """ Set up a new instance. """
        self._enumtype = enumtype
        self._index = index
        self._key = key

    @property
    def enumtype(self):
        return self._enumtype

    @property
    def key(self):
        return self._key

    def __str__(self):
        return str(self.key)

    @property
    def index(self):
        return self._index

    def __repr__(self):
        return "EnumValue(%(_enumtype)r, %(_index)r, %(_key)r)" % vars(self)

    def __hash__(self):
        return hash(self._index)

    @_comparator
    def __eq__(self, other):
        return self == other

    @_comparator
    def __ne__(self, other):
        return self != other

    @_comparator
    def __lt__(self, other):
        return self < other

    @_comparator
    def __le__(self, other):
        return self <= other

    @_comparator
    def __gt__(self, other):
        return self > other

    @_comparator
    def __ge__(self, other):
        return self >= other


class Enum(object):
    """ Enumerated type. """

    def __init__(self, *keys, **kwargs):
        """ Create an enumeration instance. """

        value_type = kwargs.get('value_type', EnumValue)

        if not keys:
            raise EnumEmptyError()

        keys = tuple(keys)
        values = [None] * len(keys)

        for i, key in enumerate(keys):
            value = value_type(self, i, key)
            values[i] = value
            try:
                super(Enum, self).__setattr__(key, value)
            except TypeError:
                raise EnumBadKeyError(key)

        self.__dict__['_keys'] = keys
        self.__dict__['_values'] = values

    def __setattr__(self, name, value):
        raise EnumImmutableError(name)

    def __delattr__(self, name):
        raise EnumImmutableError(name)

    def __len__(self):
        return len(self._values)

    def __getitem__(self, index):
        # tony 添加，添加从字符型枚举名到变量值的转换
        if isinstance(index, str) or isinstance(index, unicode):
            return self.__getattribute__(index)
        else:
            return self._values[index]

    def __setitem__(self, index, value):
        raise EnumImmutableError(index)

    def __delitem__(self, index):
        raise EnumImmutableError(index)

    def __iter__(self):
        return iter(self._values)

    def __contains__(self, value):
        is_member = False
        if isinstance(value, basestring):
            is_member = (value in self._keys)
        else:
            is_member = (value in self._values)
        return is_member
