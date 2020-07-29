# class Domain:
#     local_dict_of_domains = {'heat': __name__, 'cool': __name__}
#     # Чтобы не ругался
#
#     def __new__(cls, *args, **kwargs):
#         obj = super().__new__(cls)
#         cls.local_dict_of_domains[kwargs['state']] = obj
#         return obj
#
#     def __init__(self, num, state):
#         self.app = num
#         self.can = self.appen()
#
#     def appen(self):
#         return self.app * 2
#
#
# a = Domain(1, state='heat')
# b = Domain(100, state='cool')
# print(Domain.local_dict_of_domains)
#
# a.__init__(1000000, state='heat')
# print(a is Domain.local_dict_of_domains['heat'])
# print(Domain.local_dict_of_domains['heat'].app)
# print(a.app)
#
#
#
#
#
