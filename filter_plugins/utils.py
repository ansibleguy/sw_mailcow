from re import match as regex_match
from re import compile as regex_compile


class FilterModule(object):

    def filters(self):
        return {
            "valid_hostname": self.valid_hostname,
        }

    @staticmethod
    def valid_hostname(name: str) -> bool:
        # see: https://validators.readthedocs.io/en/latest/_modules/validators/domain.html
        domain = regex_compile(
            r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
            r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
            r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
            r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
        )
        valid_domain = True if domain.match(name) is not None else False
        # see: https://en.wikipedia.org/wiki/Hostname#Restrictions_on_valid_host_names
        expr_hostname = r'^[a-zA-Z0-9-\.]{1,253}$'
        valid_hostname = True if regex_match(expr_hostname, name) is not None else False
        return all([valid_domain, valid_hostname])
