import example
import exampleClasses


def stringMatch(R: ParseRec, s: str):
    return R.s.strip() == s
