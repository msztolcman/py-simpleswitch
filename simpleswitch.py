__all__ = ['switch']

class _case:
    def __init__(self, switch):
        self.switch = switch

    def _get_args(self, args):
        return list(self.switch.callback_args) + list(args)

    def _get_kwargs(self, kwargs):
        ret = self.switch.callback_kwargs.copy()
        ret.update(kwargs)
        return ret

    def __call__(self, assrt, callback=None, pass_through=False, *args, **kwargs):
        if self.switch.is_exhausted:
            return

        if self.switch.auto_assert:
            assrt = assrt == self.switch.value

        if assrt or self.switch.pass_through:
            self.switch.pass_through = pass_through

            if not pass_through:
                self.switch.is_exhausted = True

            if callback:
                callback(self.switch.value, *self._get_args(args), **self._get_kwargs(kwargs))

    def default(self, callback):
        if self.switch.is_exhausted:
            return

        if callback:
            callback(self.switch.value)


class switch:
    def __init__(self, value, simple=False, args=None, kwargs=None):
        self.value = value
        self.is_exhausted = False
        self.pass_through = False
        self.auto_assert = simple
        self.callback_args = args or []
        self.callback_kwargs = kwargs or {}

    def __enter__(self, *a, **b):
        return _case(self)

    def __exit__(self, *a, **b):
        pass

