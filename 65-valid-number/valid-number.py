class Solution:
    def isNumber(self, s: str) -> bool:
        if s[0] == "e" or s[0] == "E":
            return False

        digit = False
        dot = False
        exp = False

        for i in range(len(s)):
            if s[i].isdigit():
                digit = True

            elif s[i] == ".":
                if dot or exp:
                    return False
                dot = True

            elif s[i] == "e" or s[i] == "E":
                if exp or not digit:
                    return False
                exp = True
                digit = False

            elif s[i] == "+" or s[i] == "-":
                if i != 0 and s[i - 1] != "e" and s[i - 1] != "E":
                    return False

            else:
                return False

        return digit