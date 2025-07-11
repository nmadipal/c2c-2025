from gpiozero.pins import data
from gpiozero import Factory, BoardInfo, HeaderInfo, PinInfo, Pin
from gpiozero import PinInvalidPin, PinInvalidState, PinSetInput, PinInvalidPull, PinPWMFixedValue
from gpiozero.compat import frozendict
from queue import Queue, Empty
from time import monotonic
from threading import RLock, Thread
from types import MethodType
from matrix_scan import MatrixScan
from weakref import ref, WeakMethod


class MatrixScanPinFactory(Factory):

    def __init__(self, matrix_scan):
        super().__init__()
        self._info = None
        self.pins = {}
        self.pin_class = MatrixScanPin
        # Factory will hold a reference to the matrix scan factory
        # MUST be configured outside and passed into the MatrixScanPinFactory object
        if not isinstance(matrix_scan, MatrixScan):
            raise NotMatrixScanError(f'matrix_scan is not a MatrixScan object')
        else:
            self.matrix_scan = matrix_scan
            # self.matrix_scan.start()
        
    def ticks(self):
        # ToDo: Consider changing
        return monotonic()

    def ticks_diff(self, later, earlier):
        # ToDo: Consider changing
        return later - earlier

    def _get_board_info(self):
        if self._info is None:
            self._info = MatrixScanBoardInfo.return_board_info()
        return self._info
            
    def close(self):
        self.matrix_scan.stop_scan_matrix()
        for pin in self.pins.values():
            pin.close()
        self.pins.clear()
        self.matrix_scan.release_scan_matrix()

    def pin(self, name):
        # header: HeaderInfo
        # info: PinInfo
        for header, info in self.board_info.find_pin(name):
            try:
                pin = self.pins[info]
            except KeyError:
                pin = self.pin_class(self, info)
                self.pins[info] = pin
                self.matrix_scan.enable_button(name)
                self.matrix_scan.set_callback(name, pin._call_when_changed)
            return pin
        raise PinInvalidPin(f'{name} is not a valid pin name')

class MatrixScanPin(Pin):

    # Arbitrary - based on LGPIO conventions
    GPIO_EDGES = {
        'both':3,
        'rising': 1,
        'falling': 2
        }
    
    def __init__(self, factory, info):
        super().__init__()
        if 'button' not in info.interfaces:
            raise PinInvalidPin(f'{info} is not a Matrix Button pin')
        self._factory = factory
        self._info = info
        self._number = int(info.name[3:])
        self._when_changed_lock = RLock()
        self._when_changed = None
        self._edges = None
        self._bounce = None
        # Dummy properties - These have no use
        self._pull = info.pull or 'floating'
        self._pwm = None
        self._frequency = None
        self._duty_cycle = None

        
    @property
    def info(self):
        return self._info

    @property
    def number(self):
        return self._info.name

    def __repr__(self):
        return self._info.name

    @property
    def factory(self):
        return self._factory

    def _get_info(self):
        return self.info

    # Matrix Scan pins cannot be outputs
    def output_with_state(self, state):
        raise PinSetInput('Matrix Pad Pin does not have an output')

    def _get_state(self):
        return self.factory.matrix_scan.get_button_state(self._number)

    def _set_state(self, value):
        raise PinInvalidState('Cannot Set State on Matrix Pad Pin')

    def _get_function(self):
        return 'input'

    def _set_function(self, value):
        if value == 'input':
            pass
        else:
            raise PinSetInput(f'Matrix Pad Pin cannot be {value} - input only')

    def _get_pull(self):
        return self._pull

    def _set_pull(self, value):
        if value != 'floating':
            raise PinInvalidPull(f'Matrix Pad Pin has no pull option {value} - must be floating')
        else:
            pass

    def _get_frequency(self):
        return self._frequency

    def _set_frequency(self, value):
        if value != None:
            raise PinPWMFixedValue('Matrix Pad Pin cannot have PWM output')
        else:
            pass

    def _get_bounce(self):
        return self.factory.matrix_scan.bounce_time

    def _set_bounce(self, value):
        f = self.when_changed
        self.when_changed = None
        self.factory.matrix_scan.update_bounce_time(value)
        self.when_changed = f

    def _get_edges(self):
        return self._edges

    def _set_edges(self, value):
        f = self.when_changed
        self.when_changed = None
        self._edges = value
        self.factory.matrix_scan.set_button_edge_trig(self._number, value)
        self.when_changed = f
        
    # Copied from PiPin class, not sure if this is correct
    def _call_when_changed(self, ticks=None, state=None):
        method = self._when_changed()
        if method is None:
            self.when_changed = None
        else:
            if ticks == None:
                ticks = self.factory.ticks()
            if state == None:
                state = self.state
            method(ticks, state)

    def _get_when_changed(self):
        # print('DEBUG: In _get_when_changed')
        return None if self._when_changed is None else self._when_changed()

    def _set_when_changed(self, value):
        # print('DEBUG: In _set_when_changed')
        with self._when_changed_lock:
            if value is None:
                if self._when_changed is not None:
                    self._disable_event_detect()
                self._when_changed = None
            else:
                enabled = self._when_changed is not None
                if isinstance(value, MethodType):
                    self._when_changed = WeakMethod(value)
                else:
                    self._when_changed = ref(value)
                if not enabled:
                    self._enable_event_detect()

    
    def _enable_event_detect(self):
        # print('DEBUG: enable_event_detect')
        self.factory.matrix_scan.watch_button(self._number, self._edges)


    def _disable_event_detect(self):
        # print('DEBUG: disable_event_detect')
        self.factory.matrix_scan.unwatch_button(self._number)
        
        
        

class MatrixScanBoardInfo(BoardInfo):
    __slots__ = () # workaround python issue #24931

    @classmethod
    def return_board_info(cls):
        headers = cls.generate_matrix_header()
        board = data.BPLUS_BOARD
        return cls(
            revision='a02082', # Dummy revision - Taken from gpiozero mock.py
            model='???', # Dummy model
            pcb_revision='Unknown', # Dummy pcb revision
            released='Unknown', # Dummy released
            soc='Unknown', # Dummy soc
            manufacturer='Unknown', # Dummy manufacturer
            memory=None, # Dummy memory
            storage='MicroSD', # Dummy storage
            usb=4, # Dummy usb
            usb3=0, # Dummy usb3
            ethernet=1, # Dummy ethernet
            eth_speed=0, # Dummy eth_speed
            wifi=False, # Dummy wifi
            bluetooth=False, # Dummy bluetooth
            csi=1, # Dummy csi
            dsi=1, # Dummy dsi
            headers=headers,
            board=board # Dummy board
            )

    @classmethod
    def generate_matrix_header(cls):
        header = 'Matrix Pad'
        rows = 4
        columns = 4

        header_data = {}
        pin_list = []
        
        pin_idx = 0
        for row in range(rows):
            for col in range(columns):
                pin_idx += 1
                pin_name = f'BTN{pin_idx}'
                header_data[pin_idx] = {'button': pin_name}
                # pin_list.append({'button': pin_name})
                
        
        # header_data = {
        #     1: 1, 2: 2, 3: 3, 4: 4,
        #     5: 5, 6: 6, 7: 7, 8: 8,
        #     9: 9, 10: 10, 11: 11, 12: 12,
        #     13: 13, 14: 14, 15: 15, 16: 16
        # }

        headers = frozendict({
            header: HeaderInfo(
                name = header, rows=rows, columns=columns,
                pins=frozendict({
                    number: cls._make_pin(
                        header, number, row + 1, col + 1, functions)
                    for number, functions in header_data.items()
                    for row in range(rows)
                    for col in range(columns)
                    })
            )
        })
        return headers

    @staticmethod
    def _make_pin(header, number, row, col, interfaces):
        name = interfaces['button']
        names = {f'{header}:{name}'}
        button = int(name[3:])
        names.add(button)
        names.add(str(button))
        names.add(f'BUTTON{button}')
        names.add(f'BTN{button}')
        pull = 'floating'
        return PinInfo(
            number=number, name=name, names=frozenset(names), pull=pull,
            row=row, col=col, interfaces=frozenset(interfaces))    
    
                
class NotMatrixScanError(Exception):
    "Error raised when a MatrixPinFactory is not passed a MatrixScan object"
 
