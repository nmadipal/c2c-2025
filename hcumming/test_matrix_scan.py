from gpiozero import Button, ButtonBoard
from matrix_scan import MatrixScan, MatrixScanButton
from matrix_scan_pin_factory import MatrixScanPinFactory, MatrixScanPin, MatrixScanBoardInfo
from signal import pause

button_count = 16
matrix_scan = MatrixScan()
factory = MatrixScanPinFactory(matrix_scan)
matrix_board = ButtonBoard(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, pull_up=None, active_state=True, pin_factory=factory)

# for button in range(16):
#     matrix_board[button].when_pressed = lambda: print(f'Button {int(button+1)} Pressed')
#     matrix_board[button].when_held = lambda: print(f'Button {int(button+1)} Held')
#     matrix_board[button].when_released = lambda: print(f'Button {int(button+1)} Released')

    
# for button in range(16):
#     matrix_board[button].when_pressed = lambda: print('Button ' + str(button + 1) + ' Pressed')
#     matrix_board[button].when_held = lambda: print('Button ' + str(button + 1) + ' Held')
#     matrix_board[button].when_released = lambda: print('Button ' + str(button + 1) + ' Released')

matrix_board[0].when_pressed = lambda: print('Button 1 Pressed')
matrix_board[1].when_pressed = lambda: print('Button 2 Pressed')
matrix_board[2].when_pressed = lambda: print('Button 3 Pressed')
matrix_board[3].when_pressed = lambda: print('Button 4 Pressed')
matrix_board[4].when_pressed = lambda: print('Button 5 Pressed')
matrix_board[5].when_pressed = lambda: print('Button 6 Pressed')
matrix_board[6].when_pressed = lambda: print('Button 7 Pressed')
matrix_board[7].when_pressed = lambda: print('Button 8 Pressed')
matrix_board[8].when_pressed = lambda: print('Button 9 Pressed')
matrix_board[9].when_pressed = lambda: print('Button 10 Pressed')
matrix_board[10].when_pressed = lambda: print('Button 11 Pressed')
matrix_board[11].when_pressed = lambda: print('Button 12 Pressed')
matrix_board[12].when_pressed = lambda: print('Button 13 Pressed')
matrix_board[13].when_pressed = lambda: print('Button 14 Pressed')
matrix_board[14].when_pressed = lambda: print('Button 15 Pressed')
matrix_board[15].when_pressed = lambda: print('Button 16 Pressed')

matrix_board[0].when_released = lambda: print('Button 1 Released')
matrix_board[1].when_released = lambda: print('Button 2 Released')
matrix_board[2].when_released = lambda: print('Button 3 Released')
matrix_board[3].when_released = lambda: print('Button 4 Released')
matrix_board[4].when_released = lambda: print('Button 5 Released')
matrix_board[5].when_released = lambda: print('Button 6 Released')
matrix_board[6].when_released = lambda: print('Button 7 Released')
matrix_board[7].when_released = lambda: print('Button 8 Released')
matrix_board[8].when_released = lambda: print('Button 9 Released')
matrix_board[9].when_released = lambda: print('Button 10 Released')
matrix_board[10].when_released = lambda: print('Button 11 Released')
matrix_board[11].when_released = lambda: print('Button 12 Released')
matrix_board[12].when_released = lambda: print('Button 13 Released')
matrix_board[13].when_released = lambda: print('Button 14 Released')
matrix_board[14].when_released = lambda: print('Button 15 Released')
matrix_board[15].when_released = lambda: print('Button 16 Released')

matrix_board[0].when_held = lambda: print('Button 1 Held')
matrix_board[1].when_held = lambda: print('Button 2 Held')
matrix_board[2].when_held = lambda: print('Button 3 Held')
matrix_board[3].when_held = lambda: print('Button 4 Held')
matrix_board[4].when_held = lambda: print('Button 5 Held')
matrix_board[5].when_held = lambda: print('Button 6 Held')
matrix_board[6].when_held = lambda: print('Button 7 Held')
matrix_board[7].when_held = lambda: print('Button 8 Held')
matrix_board[8].when_held = lambda: print('Button 9 Held')
matrix_board[9].when_held = lambda: print('Button 10 Held')
matrix_board[10].when_held = lambda: print('Button 11 Held')
matrix_board[11].when_held = lambda: print('Button 12 Held')
matrix_board[12].when_held = lambda: print('Button 13 Held')
matrix_board[13].when_held = lambda: print('Button 14 Held')
matrix_board[14].when_held = lambda: print('Button 15 Held')
matrix_board[15].when_held = lambda: print('Button 16 Held')

print('Press Ctrl-C to close the test')
pause()

matrix_scan.stop_scan_matrix()
matrix_board.close()
