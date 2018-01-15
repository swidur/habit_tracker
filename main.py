import activities
import activity

print('Welcome to habit tracker! What would you like to do? ')

actv = activities.Activities()

def main():

    while True:
        print('\nShow current habits [1]\nAdd new habit [2]\nDelete habit [3] \nExit [4] ')
        user_inpt1 = raw_input()

        try:
            ask = int(user_inpt1)
        except (TypeError, ValueError):
            print('Expected number, got {}'.format(type(user_inpt1)))
            main()

        if ask == 1:
            actv.get_aggregated()

        elif ask == 2:
            user_inpt2 = raw_input('What did you do? ')
            try:
                act_name = str(user_inpt2)
            except (TypeError, ValueError):
                print('Expected string, got {}'.format(type(user_inpt2)))

            user_inpt3 = raw_input('How long? (hrs) ')
            try:
                duration = int(user_inpt3)
            except (TypeError, ValueError):
                print('Expected number, got {}'.format(type(user_inpt3)))

            try:
                actv.add_act(activity.Activity(act_name,duration))
            except UnboundLocalError:
                pass

        elif ask == 3:
            user_inpt5 = raw_input('Delete an entry by ID [1]\nDelete activity by name [2]\nBack to main menu [0] ')

            try:
                id_or_name = int(user_inpt5)
            except (TypeError, ValueError):
                print('Expected number, got {}'.format(type(user_inpt5)))
                main()

            if id_or_name == 1:
                actv.get_entries()
                user_inpt4 = raw_input('Which entry would you like to delete? [ID] ')
                try:
                    rmv = int(user_inpt4)
                except (TypeError, ValueError):
                    print('Expected number, got {}'.format(type(user_inpt4)))
                actv.del_by_id(rmv)

            elif id_or_name == 2:
                actv.get_aggregated()
                user_inpt4 = raw_input('Which activity would you like to delete? [Name] ')
                try:
                    rmv = str(user_inpt4)
                except (TypeError, ValueError):
                    print('Expected string, got {}'.format(type(user_inpt4)))
                actv.del_by_name(rmv)

            elif id_or_name == 0:
                main()

        elif ask == 4:
            actv.close_connection()
            quit()

main()
