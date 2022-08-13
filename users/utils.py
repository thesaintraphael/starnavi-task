import string
import random

from .models import User


class UserCodeUtil:

    size: int = 6

    @classmethod
    def genearte_code(cls) -> str:
        return "".join(random.choice(string.digits) for _ in range(cls.size))

    @classmethod
    def genearte_act_code(cls) -> str:
        code = cls.genearte_code()

        if User.objects.filter(activation_code=code).exists():
            return cls.genearte_act_code()

        return code

    @classmethod
    def genearte_reset_code(cls) -> str:
        code = cls.genearte_code()

        if User.objects.filter(reset_code=code).exists():
            return cls.genearte_reset_code()

        return code
