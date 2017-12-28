import tracker

print('Welcome to habit tracker! What would you like to do? ')


def main():
    while True:
        print('\nShow current habits [1] ')
        print('Add new habit [2]')
        print ('Remove habit [3] \n')

        user_inpt1 = raw_input()

        try:
            ask = int(user_inpt1)
        except (TypeError, ValueError):
            print('Expected number, got {}'.format(type(user_inpt1)))
            main()

        if ask == 1:
            tracker.get_activ_names()

        elif ask == 2:
            user_inpt2 = raw_input('What did you do? ')
            try:
                activity = str(user_inpt2)
            except (TypeError, ValueError):
                print('Expected string, got {}'.format(type(user_inpt2)))

            user_inpt3 = raw_input('How long? (hrs) ')
            try:
                duration = int(user_inpt3)
            except (TypeError, ValueError):
                print('Expected number, got {}'.format(type(user_inpt3)))

            try:
                tracker.add_activ(activity, duration)
            except UnboundLocalError:
                pass

        elif ask == 3:
            tracker.get_activ_names()
            user_inpt4 = raw_input('Which activity would you like to delete? [num]')
            try:
                rmv = int(user_inpt4)
            except (TypeError, ValueError):
                print('Expected number, got {}'.format(type(user_inpt4)))
            tracker.rmv_activ(rmv)


main()
