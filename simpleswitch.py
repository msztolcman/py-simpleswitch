__all__ = ['switch']

__version__ = '0.1'

class _case:
    """ `_case` class realizes case statement in `switch`.
        Is returned to context manager from `switch` class, and is used as
        callable, or it's `default` method.
    """

    def __init__(self, switch):
        """ Initialize object
        """
        self.switch = switch

    def _get_args(self, args):
        """ Build positional arguments for callback, using common
            (defined in `switch`) and local (passed to `case`) arguments.
        """
        return list(self.switch.callback_args) + list(args)

    def _get_kwargs(self, kwargs):
        """ Build keyword arguments for callback, using common
            (defined in `switch`) and local (passed to `case`) arguments.
        """
        ret = self.switch.callback_kwargs.copy()
        ret.update(kwargs)
        return ret

    def __call__(self, assrt, callback=None, pass_through=False, *args, **kwargs):
        """ Test `case` condition and if it's evaluated to true (or was evaluated
            in previous statement, and is enabled `pass_through`), call defined
            action.
        """

        if self.switch.is_finished:
            raise Exception('Using case aside of context manager it was definied is denied')

        if self.switch.is_exhausted:
            return

        assrt = self.switch.asserter(assrt)

        if assrt or self.switch.pass_through:
            self.switch.pass_through = pass_through

            ## save info about resolved condition, if pass_through wais False
            if not pass_through:
                self.switch.is_exhausted = True

            ## call callback if given
            if callback:
                callback(self.switch.value, *self._get_args(args), **self._get_kwargs(kwargs))

    def default(self, callback=None):
        """ `default` statement in `switch` clause.
        """
        if self.switch.is_exhausted:
            return

        if callback:
            callback(self.switch.value)


class switch:
    """ `switch` clause. For use in context manager.
        Also common storage for all `case` statements.
    """
    def __init__(self, value, asserter=None, args=None, kwargs=None):
        """ Initializes data, and determine asserter in case when `asserter` is not
            callable.
        """
        self.value = value
        self.is_exhausted = False
        self.pass_through = False
        self.callback_args = args or []
        self.callback_kwargs = kwargs or {}
        self.is_finished = False

        if asserter is None:
            self.asserter = bool
        elif hasattr(asserter, '__call__'):
            self.asserter = asserter
        elif asserter == True:
            self.asserter = lambda val: val == value
        else:
            raise TypeError('Can\'t use given asserter: %r' % (asserter, ))

    def __enter__(self, *a, **b):
        """ Realizes context manager API.
            Returns _case instance with bounded `switch` (for common storage purposes)
        """
        return _case(self)

    def __exit__(self, *a, **b):
        """ Mark switch as finished when exits from context manager.
        """
        self.is_exhausted = True
        self.is_finished = True

