from button_pad import ButtonPad

def print_button_state(button_state):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in button_state]))
    print(' ')

btn_pad = ButtonPad()


while True:
    btn_pad.read_buttons()
    btn_pad.display_buttons()
    # print_button_state(button_state)
    

