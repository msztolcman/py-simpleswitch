py-simpleswitch
===============

Simple proof of concept of switch for python.

Usage
=====

    from simpleswitch import switch

    def callback1(val):
        print('RESULT1:', val)
    def callback2(val):
        print('RESULT2:', val)
    def callback3(val):
        print('RESULT3:', val)
    def callback4(val):
        print('RESULT4:', val)
    def callback_default(val):
        print('RESULT DEFAULT:', val)

    a = 2
    with switch(a) as case:
        case(a == 1, callback1, pass_through=True)
        case(a == 2, callback2, pass_through=True)
        case(a == 3, callback3, pass_through=False)
        case(a == 4, callback4)
        case.default(callback_default)

    with switch(a, True) as case:
        case(1, callback1, pass_through=True)
        case(2, callback2, pass_through=True)
        case(3, callback3, pass_through=False)
        case(4, callback4)
        case.default(callback_default)

    def callback5(val, arg1, arg2):
        print('RESULT5: %s!%s!%s' % (val, arg1, arg2))

    with switch(a, args=('q', )) as case:
        case(a == 1, callback1)
        case(a == 2, callback5, False, 'w')

    def callback6(val, arg1, arg2):
        print('RESULT6: %s!%s!%s' % (val, arg1, arg2))

    with switch(a, kwargs={'arg1': 'q'}) as case:
        case(a == 1, callback1)
        case(a == 2, callback6, False, arg2 = 'w')

    with switch(a, bool) as case:
        case(1, callback1, pass_through=True)
        case(2, callback2, pass_through=True)
        case(3, callback3, pass_through=False)
        case(4, callback4)
        case.default(callback_default)

    with switch(a, lambda v: not (v % 2)) as case:
        case(1, callback1, pass_through=True)
        case(2, callback2, pass_through=True)
        case(3, callback3, pass_through=False)
        case(4, callback4)
        case.default(callback_default)

    with switch(None, 'asd'.__eq__) as case:
        case('ASD', callback1, pass_through=True)
        case('asd', callback2, pass_through=True)
        case('qwe', callback3, pass_through=False)
        case(4, callback4)
        case.default(callback_default)
