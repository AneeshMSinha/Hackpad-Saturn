# Saturn kmk code v1
import board
import busio


from kmk.handlers.sequences import send_string
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.layers import Layers

# OLED libraries must be present in CIRCUITPY/lib:
# - adafruit_ssd1306.mpy
# - adafruit_bus_device/
# - adafruit_framebuf.mpy (if required)
try:
    import adafruit_ssd1306
    OLED_AVAILABLE = True
except ImportError:
    OLED_AVAILABLE = False


keyboard = KMKKeyboard()

# --------------------
# MATRIX (from your PCB)
# Cols: D0 D1 D2 D3
# Rows: D6 D7 D8
# Diodes: COL2ROW
# --------------------
keyboard.col_pins = (
    board.D0,
    board.D1,
    board.D2,
    board.D3,
)
keyboard.row_pins = (
    board.D6,
    board.D7,
    board.D8,
)
keyboard.diode_orientation = keyboard.DIODE_COL2ROW


# --------------------
# LAYERS MODULE
# --------------------
layers = Layers()
keyboard.modules.append(layers)


# --------------------
# ROTARY ENCODER (rotation only)
# A: D9, B: D10
# Encoder press is part of matrix
# --------------------
encoder = EncoderHandler()
keyboard.modules.append(encoder)

encoder.pins = (
    (board.D9, board.D10, None),
)

# Encoder behavior per layer
encoder.map = [
    ((KC.VOLD, KC.VOLU),),        # Layer 0
    ((KC.LEFT, KC.RIGHT),),       # Layer 1
]


# --------------------
# OLED (I2C on D4/D5)
# SDA = D4, SCL = D5
# --------------------
oled = None
if OLED_AVAILABLE:
    try:
        i2c = busio.I2C(board.D5, board.D4)  # SCL, SDA
        try:
            oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
        except Exception:
            oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3D)

        oled.fill(0)
        oled.text("SATURN v1", 0, 0, 1)
        oled.text("Layer 0", 0, 12, 1)
        oled.show()
    except Exception:
        oled = None


GMAIL = KC.MACRO(
    KC.LGUI(KC.T),        # Cmd + T (new tab)
    KC.LGUI(KC.L),        # Cmd + L (focus address bar)
    send_string("gmail.com"),
    KC.ENTER,
)

SCHOOLOGY = KC.MACRO(
    KC.LGUI(KC.T),        # Cmd + T (new tab)
    KC.LGUI(KC.L),        # Cmd + L (focus address bar)
    send_string("https://fuhsd.schoology.com/home#/?_k=9wc02e"),
    KC.ENTER,
)

CHATGPT = KC.MACRO(
    KC.LGUI(KC.T),        # Cmd + T (new tab)
    KC.LGUI(KC.L),        # Cmd + L (focus address bar)
    send_string("chatgpt.com"),
    KC.ENTER,
)

SCREENSHOT = KC.MACRO(
	KC.LGUI(KC.SHIFT(KC.N4))
)

# --------------------
# KEYMAP (3 x 4)
# Top-right key = KC.TO(1)
# Layer 1 top-right = KC.TO(0) (safe return)
# --------------------
keyboard.keymap = [
    [   # -------- Layer 0 (Base) --------
        KC.MUTE, KC.COPY, KC.CUT, KC.TO(1),
        KC.PASTE,  KC.COPY,  KC.PASTE,  KC.LGUI(KC.T),
        SCREENSHOT,  SCHOOLOGY,  GMAIL,  CHATGPT,
    ],
    [   # -------- Layer 1 (Alt) --------
        KC.MUTE, KC.F2, KC.F1, KC.TO(0),
        KC.LEFT, KC.RIGHT, KC.UP, KC.F3,
        KC.MPRV, KC.MPLAY, KC.MNXT, KC.DOWN,
    ],
]


# --------------------
# OPTIONAL: OLED layer update
# --------------------
if oled:
    def before_matrix_scan():
        oled.fill(0)
        oled.text("SATURN v1", 0, 0, 1)
        oled.text("Layer {}".format(layers.active_layers[0]), 0, 12, 1)
        oled.show()

    keyboard.before_matrix_scan = before_matrix_scan


if __name__ == "__main__":
    keyboard.go()
