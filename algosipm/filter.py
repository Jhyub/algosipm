from enum import Enum

from algosipm.element import Element


class Filter:
    def __init__(self):
        pass

    def check(self, element: Element) -> bool:
        pass


class FilterChainConnection(Enum):
    AND = 0
    OR = 1


class FilterChain(Filter):
    def __init__(self, ss: list[(int, str)]):
        super(FilterChain, self).__init__()
        self.empty = False
        self.error = ""
        if len(ss) == 0:
            self.empty = True
            return
        if not "".join(map(lambda x: x[1], ss)):
            self.empty = True
            return
        (f1, f2, fcc) = self.parse(ss)
        self.f1 = f1
        self.f2 = f2
        self.fcc = fcc

    @staticmethod
    def fromQuery(query: str):
        return FilterChain(list(enumerate(query.strip().split(" "))))

    def parse(self, ss: list[(int, str)]) -> (Filter, Filter, FilterChainConnection):
        print(f"debug / {ss}")
        if ss[0][1] == "and":
            self.error = f"Error at word #{ss[0][0]} '{ss[0][1]}': unexpected 'and'"
        elif ss[0][1] == "or":
            self.error = f"Error at word #{ss[0][0]} '{ss[0][1]}': unexpected 'or'"
        elif len(ss[0][1]) == 0:
            self.error = f"Error at word #{ss[0][0]} '{ss[0][1]}': inappropriate empty token"
        elif ss[0][1][0] == "!":  # Catch not
            if len(ss[0][1]) == 1:
                self.error = f"Error at word #{ss[0][0]} '{ss[0][1]}': unfinished not expression"
            else:
                ss[0] = (ss[0][0], ss[0][1][1:])
                (f1, f2, fcc) = self.parse(ss)
                return Not(f1), f2, fcc
        elif ss[0][1][0] == "(":
            (inside, leftover) = self.catchParentheses(ss)
            return self.handleLeftover(inside, leftover, (FilterChain(inside), Empty(), FilterChainConnection.AND))
        elif len(ss) >= 2 and ss[0][1][-1] == ":":
            (attribute, leftover) = self.catchAttribute(ss)
            return self.handleLeftover(attribute, leftover, (AttributeFilter(attribute[0][1][:-1], attribute[1][1]), Empty(), FilterChainConnection.AND))
        elif len(ss) >= 1:
            (name, leftover) = self.catchName(ss)
            return self.handleLeftover(name, leftover, (NameFilter(name[0][1]), Empty(), FilterChainConnection.AND))

        if not self.error:
            self.error = "What?"
        return Empty(), Empty(), FilterChainConnection.AND

    def handleLeftover(self, caught, leftover, returnval):
        if len(leftover) == 0:
            return returnval
        if leftover[0][1] == "and":
            if len(leftover) == 1:
                self.error = f"Error at word #{leftover[0][0]} '{leftover[0][1]}': unexpected dead end"
            return FilterChain(caught), FilterChain(leftover[1:]), FilterChainConnection.AND
        if leftover[0][1] == "or":
            if len(leftover) == 1:
                self.error = f"Error at word #{leftover[0][0]} '{leftover[0][1]}': unexpected dead end"
            return FilterChain(caught), FilterChain(leftover[1:]), FilterChainConnection.OR
        self.error = f"Error at word #{leftover[0][0]} '{leftover[0][1]}': expected 'and' or 'or'"
        return Empty(), Empty(), FilterChainConnection.AND

    """
    We have some issues with parentheses
    * how to group?
    * how to work around with spaces? (looks irregular)
    """
    def catchParentheses(self, ss: list[(int, str)]) -> (list[(int, str)], list[(int, str)]):
        idx = -1
        cnt = 0
        for (idxs, (i, j)) in enumerate(ss):
            if len(j) == 0:
                continue
            k = 0
            while j[k] == "(":
                cnt += 1
                k += 1
                if k >= len(j):
                    break
            k = -1
            while j[k] == ")":
                cnt -= 1
                k -= 1
                idx = idxs
                if -k > len(j):
                    break
        if cnt != 0:
            self.error = f"Error at word #{ss[0][0]} '{ss[0][1]}': unclosed parentheses"
            return [], []
        ss[0] = (ss[0][0], ss[0][1][1:])
        ss[idx] = (ss[idx][0], ss[idx][1][:-1])
        if len(ss[idx][1]) == 0:
            return ss[0:idx], ss[idx+1:]
        return ss[0:idx+1], ss[idx+1:]

    def catchAttribute(self, ss: list[(int, str)]) -> (list[(int, str)], list[(int, str)]):
        if len(ss[0][1][0:-1]) == 0:
            self.error = f"Error at word #{ss[0][0]} '{ss[0][1]}': attribute name not specified"
        if ss[0][1][0] in ['(', ')', '!', '&', '|']:
            self.error = f"Error at word #{ss[0][0]} '{ss[0][1]}': unexpected attribute name start {ss[0][1][0]}"
        return ss[0:2], ss[2:]

    def catchName(self, ss: list[(int, str)]) -> (list[(int, str)], list[(int, str)]):
        return ss[0:1], ss[1:]

    def errorMessage(self) -> str:
        return self.error

    def check(self, element: Element) -> bool:
        if self.empty:
            return True
        if self.error:
            return True

        if self.fcc == FilterChainConnection.AND:
            return self.f1.check(element) and self.f2.check(element)
        elif self.fcc == FilterChainConnection.OR:
            return self.f1.check(element) or self.f2.check(element)


class Not(Filter):
    def __init__(self, f: Filter):
        super(Not, self).__init__()
        self.filter = f

    def check(self, element: Element) -> bool:
        return not self.filter.check(element)


class Empty(Filter):
    def __init__(self):
        super().__init__()

    def check(self, element: Element) -> bool:
        return True


class NameFilter(Filter):
    def __init__(self, query: str):
        super(NameFilter, self).__init__()
        self.query = query
        self.exact = False
        if query[0] == "\"" and query[-1] == "\"" and len(query) >= 2:
            self.exact = True

    def check(self, element: Element) -> bool:
        if self.exact:
            return self.query[1:-1].lower() == element.name.lower()
        # Fuzzy Search
        ptr = 0
        flag = True
        for i in self.query.lower():
            while ptr < len(element.name.lower()):
                if i == element.name.lower()[ptr]:
                    break
                else:
                    ptr += 1
            if ptr == len(element.name.lower()):
                flag = False
                break
        return flag


class AttributeFilter(Filter):
    def __init__(self, attributeName: str, value: str):
        super(AttributeFilter, self).__init__()
        print(f"debug / attribute name: {attributeName}, value: {value}")
        self.name = attributeName
        self.value = value

    def check(self, element: Element) -> bool:
        if self.name == "name":
            return self.value.lower() == element.name.lower()
        if self.name == "symbol":
            return self.value.lower() == element.symbol.lower()
        if self.name == "period":
            if self.value.isdigit():
                if element.period in [8, 9]:
                    return int(self.value) == element.period-2
                return int(self.value) == element.period
            return False
        if self.name == "group":
            if element.period in [8, 9]:
                if self.value.isdigit():
                    return False
            if self.value.lower() == "la":
                return 8 == element.period
            if self.value.lower() == "ac":
                return 9 == element.period
            if self.value.isdigit():
                return int(self.value) == element.group
            return False
        if self.name == "metal":
            if self.value.lower() == "nonmetal":
                return 0 == element.metal
            if self.value.lower() == "metalloid":
                return 1 == element.metal
            if self.value.lower() == "metal":
                return 2 == element.metal
            if self.value.lower() == "unknown":
                return 3 == element.metal
            return False
        return True

