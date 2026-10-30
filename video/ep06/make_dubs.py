"""Source of video/ep06/dub/{hi,pt,es}.json (the Turkish dub, spelled phonetically, is edited in dub/tr.json).
Numbers are spelled out in words so the length check below measures what the voice really says.
Usage: python video/ep06/make_dubs.py"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
IDS = [s["id"] for s in json.loads((ROOT / "script.json").read_text(encoding="utf-8"))["segments"]]

HI = [
    # s01
    "\u090f\u0915 LED, \u091c\u094b \u0930\u0902\u0917 \u0906\u092a \u091a\u093e\u0939\u0947\u0902\u0964 \u0932\u093e\u0932, \u0939\u0930\u093e, \u0928\u0940\u0932\u093e, \u0914\u0930 \u090f\u0915 \u092c\u093e\u0930 \u0926\u092c\u093e\u0924\u0947 \u0939\u0940 \u0928\u0940\u0932\u0947 \u0938\u0947 \u0932\u093e\u0932 \u0924\u0915 \u0927\u0940\u092e\u093e \u092c\u0926\u0932\u093e\u0935\u0964",
    # s02
    "\u0907\u0938 video \u0915\u0947 \u0905\u0902\u0924 \u0924\u0915 \u0906\u092a \u0905\u092a\u0928\u0947 \u0930\u0902\u0917 \u0916\u0941\u0926 \u092e\u093f\u0932\u093e\u090f\u0901\u0917\u0947, \u0914\u0930 \u090f\u0915 \u092c\u091f\u0928 \u0909\u0928\u092e\u0947\u0902 \u0938\u0947 \u091a\u0941\u0928\u0947\u0917\u093e\u0964",
    # s03
    "\u092a\u0939\u0932\u0947, \u092a\u093f\u091b\u0932\u0947 episode \u0938\u0947 \u0926\u094b \u0938\u0935\u093e\u0932\u0964 \u091b\u094b\u091f\u093e \u0938\u0935\u093e\u0932: \u090f\u0915 \u0938\u094c \u0905\u091f\u094d\u0920\u093e\u0908\u0938 \u0915\u0947 \u0938\u093e\u0925 analogWrite() LED \u0915\u093e \u0915\u094d\u092f\u093e \u0915\u0930\u0924\u093e \u0939\u0948?",
    # s04
    "pin \u0924\u0947\u091c\u093c\u0940 \u0938\u0947 \u0906\u0927\u093e \u0938\u092e\u092f on \u0939\u094b\u0924\u093e \u0939\u0948\u0964 \u0906\u0901\u0916 \u0915\u094b \u092e\u0927\u094d\u092f\u092e \u091a\u092e\u0915 \u0926\u093f\u0916\u0924\u0940 \u0939\u0948; pin \u0915\u092d\u0940 \u0906\u0927\u093e on \u0928\u0939\u0940\u0902 \u0939\u094b\u0924\u093e\u0964",
    # s05
    "\u091b\u094b\u091f\u093e \u0938\u0935\u093e\u0932: \u092c\u093f\u0928\u093e delay \u0935\u093e\u0932\u0947 fade \u092e\u0947\u0902 \u092c\u091f\u0928 \u0915\u093f\u0938\u0940 \u092d\u0940 \u092a\u0932 \u0915\u094d\u092f\u094b\u0902 \u0915\u093e\u092e \u0915\u0930\u0924\u093e \u0939\u0948?",
    # s06
    "loop \u0930\u0941\u0915\u0924\u093e \u0928\u0939\u0940\u0902: \u0918\u0921\u093c\u0940 \u0926\u0947\u0916\u0915\u0930 \u0938\u092e\u092f \u092a\u0930 \u0915\u0926\u092e, \u0939\u0930 \u091a\u0915\u094d\u0915\u0930 \u092e\u0947\u0902 \u092c\u091f\u0928 \u0915\u0940 \u091c\u093e\u0901\u091a\u0964",
    # s07
    "Episode \u092a\u093e\u0901\u091a \u0915\u093e circuit, RGB LED, \u0924\u0940\u0928 \u0914\u0930 \u0926\u094b \u0938\u094c \u092c\u0940\u0938 ohm resistors, \u0915\u0941\u091b wires \u091a\u093e\u0939\u093f\u090f\u0964",
    # s08
    "\u0905\u092a\u0928\u0947 phone \u0915\u0940 screen \u0915\u094b \u092c\u0939\u0941\u0924 \u092a\u093e\u0938 \u0938\u0947 \u0926\u0947\u0916\u093f\u090f, \u0939\u0930 \u091c\u0917\u0939 \u091b\u094b\u091f\u0947 \u0932\u093e\u0932, \u0939\u0930\u0947 \u0914\u0930 \u0928\u0940\u0932\u0947 \u092c\u093f\u0902\u0926\u0941 \u092e\u093f\u0932\u0947\u0902\u0917\u0947\u0964 \u0939\u0930 \u0930\u0902\u0917 \u0907\u0928\u094d\u0939\u0940\u0902 \u0924\u0940\u0928 \u0938\u0947 \u092c\u0928\u0924\u093e \u0939\u0948\u0964",
    # s09
    "RGB LED \u092d\u0940 \u092f\u0939\u0940 \u0939\u0948\u0964 \u0905\u0938\u0932 \u092e\u0947\u0902 \u0939\u094b\u0924\u093e \u092f\u0939 \u0939\u0948: \u090f\u0915 package \u092e\u0947\u0902 \u0924\u0940\u0928 \u091b\u094b\u091f\u0940 LEDs, \u0932\u093e\u0932, \u0939\u0930\u0940 \u0914\u0930 \u0928\u0940\u0932\u0940\u0964 \u0909\u0928\u0915\u093e \u090f\u0915 \u092a\u0948\u0930 \u0938\u093e\u091d\u093e \u0939\u0948, \u0938\u092c\u0938\u0947 \u0932\u0902\u092c\u093e \u0935\u093e\u0932\u093e\u0964",
    # s10
    "Paint \u092e\u0947\u0902 \u0932\u093e\u0932-\u0939\u0930\u093e \u092d\u0942\u0930\u093e; \u0930\u094b\u0936\u0928\u0940 \u092e\u0947\u0902 \u092f\u0939\u0940 \u092a\u0940\u0932\u093e \u0939\u0948\u0964 \u0924\u0940\u0928\u094b\u0902 \u0930\u094b\u0936\u0928\u093f\u092f\u093e\u0901 \u0938\u092b\u093c\u0947\u0926 \u092c\u0928\u093e\u0924\u0940 \u0939\u0948\u0902\u0964",
    # s11
    "USB cable \u0928\u093f\u0915\u093e\u0932\u093f\u090f, \u0914\u0930 \u090a\u092a\u0930 \u0915\u0947 breadboard \u0938\u0947 \u0939\u0930\u0940 LED \u0939\u091f\u093e\u0907\u090f\u0964 \u0939\u092e\u0947\u0902 \u0909\u0938\u0915\u093e pin \u091a\u093e\u0939\u093f\u090f, GPIO \u092a\u091a\u094d\u091a\u0940\u0938\u0964",
    # s12
    "RGB LED \u0932\u0917\u093e\u0907\u090f, \u0938\u092c\u0938\u0947 \u0932\u0902\u092c\u093e \u092a\u0948\u0930 \u092c\u093e\u090f\u0901 \u0938\u0947 \u0926\u0942\u0938\u0930\u093e\u0964 \u090f\u0915 \u0915\u093e\u0932\u093e wire \u0909\u0938 \u0932\u0902\u092c\u0947 \u092a\u0948\u0930 \u0915\u094b minus rail \u0938\u0947 \u091c\u094b\u0921\u093c\u0924\u093e \u0939\u0948\u0964",
    # s13
    "\u0939\u0930 \u0930\u0902\u0917 \u0915\u093e \u0905\u092a\u0928\u093e resistor \u0914\u0930 \u0905\u092a\u0928\u093e pin: \u0932\u093e\u0932 D \u092a\u091a\u094d\u091a\u0940\u0938 \u092a\u0930, \u0939\u0930\u093e D \u091b\u092c\u094d\u092c\u0940\u0938 \u092a\u0930, \u0914\u0930 \u0928\u0940\u0932\u093e D \u0938\u0924\u094d\u0924\u093e\u0908\u0938 \u092a\u0930\u0964",
    # s14
    "\u091b\u094b\u091f\u093e \u0938\u0935\u093e\u0932: \u0924\u0940\u0928 resistors \u0915\u094d\u092f\u094b\u0902, \u0938\u093e\u091d\u093e \u092a\u0948\u0930 \u092a\u0930 \u092c\u0938 \u090f\u0915 \u0915\u094d\u092f\u094b\u0902 \u0928\u0939\u0940\u0902?",
    # s15
    "\u0939\u0930 \u0930\u0902\u0917 \u0905\u0932\u0917 LED \u0939\u0948\u0964 \u090f\u0915 resistor, \u091c\u0948\u0938\u0947 \u0924\u0940\u0928 \u0932\u094b\u0917 \u090f\u0915 straw \u0938\u0947 \u092a\u093f\u090f\u0901: \u091c\u093c\u094b\u0930 \u0938\u0947 \u0916\u0940\u0902\u091a\u0928\u0947 \u0935\u093e\u0932\u0947 \u0915\u094b \u091c\u093c\u094d\u092f\u093e\u0926\u093e \u092e\u093f\u0932\u0947\u0964",
    # s16
    "\u0905\u0938\u0932 \u092e\u0947\u0902 \u0930\u0902\u0917 current \u092c\u093e\u0901\u091f\u0915\u0930 mix \u092c\u0926\u0932\u0924\u0947 \u0939\u0948\u0902\u0964 Straw \u0938\u0947 \u092b\u093c\u0930\u094d\u0915: \u0915\u092e voltage \u0935\u093e\u0932\u093e \u0932\u093e\u0932 \u091c\u093c\u094d\u092f\u093e\u0926\u093e \u0932\u0947\u0924\u093e \u0939\u0948\u0964",
    # s17
    "\u090f\u0915 \u092c\u093e\u0924 \u091c\u093e\u0901\u091a\u093f\u090f: \u091c\u093c\u094d\u092f\u093e\u0926\u093e\u0924\u0930 kits \u092e\u0947\u0902 common cathode LEDs \u0939\u094b\u0924\u0940 \u0939\u0948\u0902, \u0932\u0902\u092c\u093e \u092a\u0948\u0930 ground \u092a\u0930\u0964 \u0906\u092a\u0915\u0940 \u0909\u0932\u094d\u091f\u0940 \u0939\u094b, \u0924\u094b code \u092e\u0947\u0902 \u0909\u0938\u0915\u0947 \u0932\u093f\u090f \u090f\u0915 line \u0939\u0948\u0964",
    # s18
    "setColor() \u090f\u0915 helper function \u0939\u0948: coffee machine \u0915\u0947 \u092c\u091f\u0928 \u0915\u0940 \u0924\u0930\u0939 \u0924\u0940\u0928 \u092e\u093e\u0924\u094d\u0930\u093e\u090f\u0901 \u092e\u093f\u0932\u093e\u0924\u093e \u0939\u0948\u0964",
    # s19
    "\u0905\u0938\u0932 \u092e\u0947\u0902 \u0924\u0940\u0928 pins \u092a\u0930 analogWrite() \u091a\u0932\u0924\u093e \u0939\u0948: \u0939\u0930 \u0930\u0902\u0917 \u0915\u0940 \u092e\u093e\u0924\u094d\u0930\u093e \u0936\u0942\u0928\u094d\u092f \u0938\u0947 \u0926\u094b \u0938\u094c \u092a\u091a\u092a\u0928 \u0924\u0915\u0964",
    # s20
    "Coffee machine \u0938\u0947 \u092b\u093c\u0930\u094d\u0915: recipe \u092f\u093e\u0926 \u0928\u0939\u0940\u0902 \u0930\u0939\u0924\u0940; \u0924\u0940\u0928\u094b\u0902 \u092e\u093e\u0924\u094d\u0930\u093e\u090f\u0901 \u0939\u0930 \u092c\u093e\u0930 \u092c\u0924\u093e\u0907\u090f\u0964",
    # s21
    "\u091b\u094b\u091f\u093e \u0938\u0935\u093e\u0932: \u0932\u093e\u0932 \u0926\u094b \u0938\u094c \u092a\u091a\u092a\u0928, \u0939\u0930\u093e \u0936\u0942\u0928\u094d\u092f, \u0928\u0940\u0932\u093e \u0926\u094b \u0938\u094c \u092a\u091a\u092a\u0928\u0964 \u0915\u094c\u0928 \u0938\u093e \u0930\u0902\u0917 \u092c\u0928\u0947\u0917\u093e?",
    # s22
    "Magenta: \u0917\u0941\u0932\u093e\u092c\u0940 \u092c\u0948\u0902\u0917\u0928\u0940\u0964 \u0932\u093e\u0932 \u0926\u094b \u0938\u094c \u092a\u091a\u092a\u0928, \u0939\u0930\u093e \u091a\u093e\u0932\u0940\u0938 \u0930\u0916\u0947\u0902 \u0924\u094b \u0928\u093e\u0930\u0902\u0917\u0940\u0964",
    # s23
    "\u092a\u0942\u0930\u093e rgb_colors sketch: \u0924\u0940\u0928 \u0930\u0902\u0917\u094b\u0902 \u0915\u0947 \u0924\u0940\u0928 pins, \u0914\u0930 COMMON_ANODE, \u091c\u094b \u091c\u093c\u094d\u092f\u093e\u0926\u093e\u0924\u0930 kits \u092e\u0947\u0902 false \u0939\u0948\u0964",
    # s24
    "setColor() \u0924\u0940\u0928 numbers \u0932\u0947\u0924\u093e \u0939\u0948\u0964 Common anode \u092e\u0947\u0902 \u0909\u0932\u091f\u0924\u093e \u0939\u0948: \u0926\u094b \u0938\u094c \u092a\u091a\u092a\u0928 \u0915\u093e \u092e\u0924\u0932\u092c off\u0964",
    # s25
    "Loop \u092e\u0947\u0902 \u0939\u0930 line \u0915\u094b \u0932\u093e\u0932, \u0939\u0930\u093e, \u0928\u0940\u0932\u093e \u092a\u0922\u093c\u093f\u090f\u0964 Video \u0930\u094b\u0915\u093f\u090f \u0914\u0930 \u091a\u094c\u0925\u0940 line \u0915\u093e \u0905\u0902\u0926\u093e\u091c\u093c\u093e \u0932\u0917\u093e\u0907\u090f: \u0926\u094b \u0938\u094c \u092a\u091a\u092a\u0928, \u0926\u094b \u0938\u094c \u092a\u091a\u092a\u0928, \u0936\u0942\u0928\u094d\u092f\u0964 \u0915\u094c\u0928 \u0938\u093e \u0930\u0902\u0917 \u0939\u0948?",
    # s26
    "\u092a\u0942\u0930\u093e \u0932\u093e\u0932 \u0914\u0930 \u092a\u0942\u0930\u093e \u0939\u0930\u093e: \u092a\u0940\u0932\u093e\u0964 \u0939\u0930 \u0930\u0902\u0917 \u090f\u0915 second \u0930\u0939\u0924\u093e \u0939\u0948, \u0914\u0930 \u0928\u093e\u0930\u0902\u0917\u0940 \u0915\u0947 \u092c\u093e\u0926 list \u092b\u093f\u0930 \u0936\u0941\u0930\u0942 \u0939\u094b\u0924\u0940 \u0939\u0948\u0964",
    # s27
    "\u091a\u0932\u093e\u0924\u0947 \u0939\u0948\u0902: \u0932\u093e\u0932, \u0939\u0930\u093e, \u0928\u0940\u0932\u093e, \u092a\u0940\u0932\u093e, magenta, cyan, \u0938\u092b\u093c\u0947\u0926, \u0914\u0930 \u0928\u093e\u0930\u0902\u0917\u0940\u0964",
    # s27b
    "\u0927\u094d\u092f\u093e\u0928 \u0926\u0940\u091c\u093f\u090f, \u092a\u0940\u0932\u093e \u0925\u094b\u0921\u093c\u093e \u0939\u0930\u093e \u0926\u093f\u0916\u0924\u093e \u0939\u0948, \u0914\u0930 magenta \u0925\u094b\u0921\u093c\u093e \u0928\u0940\u0932\u093e\u0964 \u0924\u0940\u0928\u094b\u0902 \u0930\u0902\u0917 \u092c\u0930\u093e\u092c\u0930 \u091a\u092e\u0915\u0940\u0932\u0947 \u0928\u0939\u0940\u0902 \u0939\u0948\u0902\u0964 \u0938\u0902\u0924\u0941\u0932\u0928 \u0915\u0947 \u0932\u093f\u090f \u0939\u0930\u093e \u0914\u0930 \u0928\u0940\u0932\u093e \u0915\u092e \u0915\u0930\u0915\u0947 \u0926\u0947\u0916\u093f\u090f\u0964",
    # s28
    "\u091b\u094b\u091f\u093e \u0938\u0935\u093e\u0932: \u0930\u0902\u0917 \u092c\u0926\u0932 \u0930\u0939\u0947 \u0939\u0948\u0902\u0964 \u092f\u0939 \u0915\u093e\u0932\u093e wire \u0928\u093f\u0915\u0932 \u091c\u093e\u090f \u0924\u094b \u0915\u094d\u092f\u093e \u0939\u094b\u0917\u093e?",
    # s29
    "\u0915\u093e\u0932\u093e wire \u0928\u093f\u0915\u0932\u093e: \u0924\u0940\u0928\u094b\u0902 \u0930\u0902\u0917 \u092c\u0941\u091d \u0917\u090f\u0964 \u0935\u093e\u092a\u0938 \u0932\u0917\u093e\u090f\u0901: \u0930\u0902\u0917 \u0932\u094c\u091f\u0947\u0964",
    # s30
    "Episode \u0926\u094b: current \u0915\u094b pin \u0938\u0947 ground \u0924\u0915 \u092a\u0942\u0930\u093e \u091a\u0915\u094d\u0915\u0930 \u091a\u093e\u0939\u093f\u090f\u0964 \u0938\u093e\u091d\u093e \u092a\u0948\u0930 \u0924\u0940\u0928\u094b\u0902 \u0930\u0902\u0917\u094b\u0902 \u0915\u093e \u0905\u0915\u0947\u0932\u093e \u0935\u093e\u092a\u0938\u0940 \u0930\u093e\u0938\u094d\u0924\u093e \u0939\u0948\u0964",
    # s31
    "\u090f\u0915 \u0930\u0902\u0917 \u0928 \u091c\u0932\u0947: \u0909\u0938\u0915\u093e wire \u091c\u093e\u0901\u091a\u093f\u090f\u0964 \u0924\u0940\u0928\u094b\u0902 \u092c\u0941\u091d\u0947\u0902: \u092a\u0939\u0932\u0947 \u0938\u093e\u091d\u093e wire \u091c\u093e\u0901\u091a\u093f\u090f\u0964",
    # s32
    "TV remote \u0915\u0947 channel \u092c\u091f\u0928 \u0915\u0940 \u0924\u0930\u0939 \u0930\u0902\u0917 \u091a\u0941\u0928\u0947\u0902\u0964 mode number \u092e\u0947\u0902 \u0939\u0930 \u0928\u092f\u093e \u0926\u092c\u093e\u0935 \u090f\u0915 \u091c\u094b\u0921\u093c\u0924\u093e \u0939\u0948\u0964",
    # s33
    "\u091b\u094b\u091f\u093e \u0938\u0935\u093e\u0932: \u091a\u093e\u0930 modes \u0939\u0948\u0902, \u0936\u0942\u0928\u094d\u092f \u0938\u0947 \u0924\u0940\u0928\u0964 mode \u0924\u0940\u0928 \u0939\u0948, \u0914\u0930 \u0906\u092a \u092b\u093f\u0930 \u0926\u092c\u093e\u0924\u0947 \u0939\u0948\u0902\u0964 \u0915\u094d\u092f\u093e \u0939\u094b\u0928\u093e \u091a\u093e\u0939\u093f\u090f?",
    # s34
    "\u0936\u0942\u0928\u094d\u092f \u092a\u0930, \u091c\u0948\u0938\u0947 remote \u0906\u0916\u093c\u093f\u0930\u0940 \u0938\u0947 \u092a\u0939\u0932\u0947 channel \u092a\u0930 \u0932\u094c\u091f\u0947\u0964 \u0905\u0938\u0932 \u092e\u0947\u0902 mode \u092a\u0932 \u092d\u0930 \u091a\u093e\u0930 \u092c\u0928\u0924\u093e \u0939\u0948; \u0905\u0917\u0932\u0940 line \u0924\u0940\u0928 \u0938\u0947 \u092c\u0921\u093c\u093e \u092a\u093e\u0915\u0930 \u0909\u0938\u0947 \u0936\u0942\u0928\u094d\u092f \u0915\u0930\u0924\u0940 \u0939\u0948\u0964",
    # s35
    "Remote \u0938\u0947 \u092b\u093c\u0930\u094d\u0915: screen \u0928\u0939\u0940\u0902, mode memory \u092e\u0947\u0902 \u0939\u0948\u0964 \u091c\u093e\u0901\u091a\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0909\u0938\u0947 print \u0915\u0930\u0947\u0902\u0964",
    # s36
    "\u092f\u0939 \u0930\u0939\u093e \u092a\u0942\u0930\u093e sketch, color_modes\u0964 \u0905\u091a\u094d\u091b\u0940 \u0916\u092c\u0930: \u0907\u0938\u092e\u0947\u0902 \u0938\u091a \u092e\u0947\u0902 \u0915\u0941\u091b \u0928\u092f\u093e \u0928\u0939\u0940\u0902\u0964 \u092f\u0939 episode \u091a\u093e\u0930 \u0915\u093e \u092c\u091f\u0928, setColor(), \u0914\u0930 episode \u092a\u093e\u0901\u091a \u0915\u093e fade \u0939\u0948, \u090f\u0915 \u0938\u093e\u0925\u0964",
    # s37
    "Loop \u0915\u0947 \u0926\u0942\u0938\u0930\u0947 \u0939\u093f\u0938\u094d\u0938\u0947 \u092e\u0947\u0902 \u0939\u0930 mode \u0915\u093e \u090f\u0915 if \u0939\u0948\u0964 else if \u0915\u093e \u092e\u0924\u0932\u092c: \u0907\u0938\u0947 \u0924\u092d\u0940 \u091c\u093e\u0901\u091a\u094b \u091c\u092c \u092a\u0939\u0932\u0947 \u0935\u093e\u0932\u0947 \u0938\u092c false \u0939\u094b\u0902\u0964 \u0936\u0942\u0928\u094d\u092f \u0932\u093e\u0932, \u090f\u0915 \u0939\u0930\u093e, \u0914\u0930 \u0926\u094b \u0928\u0940\u0932\u093e\u0964",
    # s38
    "\u0906\u0916\u093c\u093f\u0930\u0940 else, mode \u0924\u0940\u0928: \u0927\u0940\u092e\u093e fade\u0964 \u0939\u0930 \u0906\u0920 milliseconds level \u090f\u0915 \u0915\u0926\u092e \u0932\u0947\u0924\u093e \u0939\u0948\u0964 \u0932\u093e\u0932 \u0915\u094b level, \u0928\u0940\u0932\u0947 \u0915\u094b \u0926\u094b \u0938\u094c \u092a\u091a\u092a\u0928 \u092e\u093e\u0907\u0928\u0938 level \u092e\u093f\u0932\u0924\u093e \u0939\u0948\u0964",
    # s39
    "Video \u0930\u094b\u0915\u093f\u090f \u0914\u0930 \u0905\u0902\u0926\u093e\u091c\u093c\u093e \u0932\u0917\u093e\u0907\u090f: fade \u0915\u0947 \u092c\u0940\u091a \u092e\u0947\u0902 level \u0915\u0930\u0940\u092c \u090f\u0915 \u0938\u094c \u0905\u091f\u094d\u0920\u093e\u0908\u0938 \u0939\u0948\u0964 \u0915\u094c\u0928 \u0938\u093e \u0930\u0902\u0917 \u0926\u093f\u0916\u0947\u0917\u093e?",
    # s40
    "\u092c\u0948\u0902\u0917\u0928\u0940: \u0906\u0927\u093e \u0932\u093e\u0932, \u0906\u0927\u093e \u0928\u0940\u0932\u093e\u0964 \u0932\u093e\u0932 \u092c\u0922\u093c\u0947, \u0928\u0940\u0932\u093e \u0918\u091f\u0947; \u0915\u0941\u0932 \u0926\u094b \u0938\u094c \u092a\u091a\u092a\u0928\u0964",
    # s41
    "\u091a\u0932\u093e\u0924\u0947 \u0939\u0948\u0902\u0964 \u0924\u0940\u0928 \u092c\u093e\u0930 \u0926\u092c\u093e\u092f\u093e: \u0932\u093e\u0932, \u0939\u0930\u093e, \u0928\u0940\u0932\u093e, \u0914\u0930 fade \u0936\u0941\u0930\u0942\u0964 \u0939\u0930 \u0926\u092c\u093e\u0935 \u0930\u0902\u0917 \u0924\u0941\u0930\u0902\u0924 \u092c\u0926\u0932\u0924\u093e \u0939\u0948, fade \u0915\u0947 \u092c\u0940\u091a \u092e\u0947\u0902 \u092d\u0940\u0964",
    # s42
    "\u0905\u092c video \u0930\u094b\u0915\u093f\u090f, \u0914\u0930 \u0905\u092a\u0928\u0947 \u0936\u092c\u094d\u0926\u094b\u0902 \u092e\u0947\u0902 \u092c\u0924\u093e\u0907\u090f \u0915\u093f \u0924\u0940\u0928 \u0915\u0947 \u092c\u093e\u0926 mode \u0936\u0942\u0928\u094d\u092f \u092a\u0930 \u0915\u094d\u092f\u094b\u0902 \u0932\u094c\u091f\u0924\u093e \u0939\u0948\u0964 \u090f\u0915 \u0935\u093e\u0915\u094d\u092f \u0915\u093e\u092b\u093c\u0940 \u0939\u0948\u0964",
    # s43
    "\u091a\u093e\u0930 modes \u0939\u0948\u0902\u0964 \u0924\u0940\u0928 \u0915\u0947 \u092c\u093e\u0926 code \u092b\u093f\u0930 \u0936\u0942\u0928\u094d\u092f \u0938\u0947 \u0936\u0941\u0930\u0942 \u0915\u0930\u0924\u093e \u0939\u0948\u0964",
    # s44
    "\u0906\u092a\u0915\u0940 \u092c\u093e\u0930\u0940: smart camping headlamp\u0964 \u091a\u093e\u0930 modes: off, \u0939\u0932\u094d\u0915\u093e \u0938\u092b\u093c\u0947\u0926, \u0924\u0947\u091c\u093c \u0938\u092b\u093c\u0947\u0926, \u0932\u093e\u0932 blink\u0964",
    # s45
    "Twist: \u0905\u0917\u0930 lamp \u0924\u0940\u0928 second \u092f\u093e \u091c\u093c\u094d\u092f\u093e\u0926\u093e \u0938\u0947 on \u0939\u0948, \u0924\u094b \u0905\u0917\u0932\u093e \u0926\u092c\u093e\u0935 \u0909\u0938\u0947 \u0938\u0940\u0927\u0947 off \u0915\u0930 \u0926\u0947\u0964 Hint: \u092f\u093e\u0926 \u0930\u0916\u093f\u090f \u0915\u093f mode \u0906\u0916\u093c\u093f\u0930\u0940 \u092c\u093e\u0930 \u0915\u092c \u092c\u0926\u0932\u093e\u0964",
    # s46
    "\u0906\u091c \u0906\u092a\u0928\u0947 \u0924\u0940\u0928 \u092c\u093e\u0924\u0947\u0902 \u0938\u0940\u0916\u0940\u0902\u0964 RGB LED \u090f\u0915 \u092e\u0947\u0902 \u0924\u0940\u0928 LEDs \u0939\u0948\u0964 setColor() \u0909\u0928\u094d\u0939\u0947\u0902 \u0924\u0940\u0928 numbers \u0938\u0947 \u092e\u093f\u0932\u093e\u0924\u093e \u0939\u0948\u0964 \u0914\u0930 mode counter \u0938\u0947 \u090f\u0915 \u092c\u091f\u0928 \u091a\u0941\u0928 \u092a\u093e\u0924\u093e \u0939\u0948\u0964",
    # s47
    "\u0905\u0917\u0932\u0940 \u092c\u093e\u0930: \u090f\u0915 knob\u0964 \u0939\u092e potentiometer \u092a\u0922\u093c\u0947\u0902\u0917\u0947, \u0914\u0930 \u0909\u0938\u0947 brightness \u092e\u0947\u0902 \u092c\u0926\u0932\u0947\u0902\u0917\u0947\u0964 \u0905\u092a\u0928\u093e headlamp comments \u092e\u0947\u0902 \u0921\u093e\u0932\u093f\u090f; \u090f\u0915 \u0939\u0932 lesson folder \u092e\u0947\u0902 \u0939\u0948\u0964 \u0935\u0939\u0940\u0902 \u092e\u093f\u0932\u0924\u0947 \u0939\u0948\u0902!",
]

PT = [
    # s01
    "Um LED: vermelho, verde, azul. Um toque inicia a lenta troca de azul a vermelho.",
    # s02
    "Voc\u00ea vai misturar cores e escolh\u00ea-las com um bot\u00e3o.",
    # s03
    "Duas perguntas: o que analogWrite() com cento e vinte e oito faz no LED?",
    # s04
    "Liga meio ciclo, bem r\u00e1pido: o olho v\u00ea brilho m\u00e9dio, mas o pino nunca fica meio ligado.",
    # s05
    "Sem delay, por que o bot\u00e3o funciona sempre?",
    # s06
    "Sem esperar, olha o rel\u00f3gio, age na hora e l\u00ea o bot\u00e3o a cada volta.",
    # s07
    "Use o circuito da aula cinco, um RGB, tr\u00eas resistores de duzentos e vinte ohms e fios.",
    # s08
    "No celular, veja os pontinhos vermelhos, verdes e azuis: toda cor da tela vem deles.",
    # s09
    "Um RGB re\u00fane tr\u00eas LEDs, vermelho, verde e azul, com a perna mais longa em comum. \u00c9 como a tela.",
    # s10
    "A luz soma: vermelho e verde d\u00e3o amarelo; as tr\u00eas, branco. Na tinta, vermelho e verde d\u00e3o marrom.",
    # s11
    "Tire USB e LED verde da protoboard de cima. Usaremos seu GPIO vinte e cinco.",
    # s12
    "Ponha a perna longa em segundo da esquerda; ligue-a ao negativo com fio preto.",
    # s13
    "Um resistor por cor: D vinte e cinco vermelho, vinte e seis verde, vinte e sete azul.",
    # s14
    "Por que tr\u00eas resistores e n\u00e3o um em comum?",
    # s15
    "Cada cor \u00e9 um LED, com corrente pr\u00f3pria. Um resistor \u00e9 um canudo para tr\u00eas: quem puxa mais ganha.",
    # s16
    "Na pr\u00e1tica, as cores disputam corrente e mudam a mistura. Diferente do canudo, ganha a cor que precisa de menos tens\u00e3o: o vermelho.",
    # s17
    "Em c\u00e1todo comum, a perna longa vai ao terra. Em \u00e2nodo comum, ajuste uma linha do c\u00f3digo.",
    # s18
    "A fun\u00e7\u00e3o auxiliar setColor() escolhe a cor. Como o bot\u00e3o da cafeteira, combina tr\u00eas ingredientes numa dose.",
    # s19
    "analogWrite() usa tr\u00eas valores, de zero a duzentos e cinquenta e cinco, um por cor.",
    # s20
    "Diferente da cafeteira, n\u00e3o lembra receitas: d\u00ea as tr\u00eas doses em cada chamada.",
    # s21
    "Vermelho e azul em duzentos e cinquenta e cinco, verde em zero: que cor d\u00e1?",
    # s22
    "Magenta, roxo rosado. Vermelho no m\u00e1ximo com quarenta de verde d\u00e1 laranja.",
    # s23
    "Em rgb_colors, s\u00e3o tr\u00eas pinos e COMMON_ANODE, em false para a maioria dos kits.",
    # s24
    "setColor() recebe tr\u00eas valores. \u00c2nodo comum os inverte: duzentos e cinquenta e cinco apaga.",
    # s25
    "No loop, leia vermelho, verde, azul. Pause: quarta linha, duas vezes duzentos e cinquenta e cinco e zero. Que cor d\u00e1?",
    # s26
    "Vermelho e verde no m\u00e1ximo d\u00e3o amarelo. Cada cor dura um segundo; ap\u00f3s laranja, repete.",
    # s27
    "Vermelho, verde, azul, amarelo, magenta, ciano, branco, laranja.",
    # s27b
    "O amarelo parece verde, e o magenta, azul: as cores t\u00eam brilhos diferentes. Reduza verde e azul para equilibrar.",
    # s28
    "Se o fio preto soltar, o que acontece \u00e0s cores?",
    # s29
    "Soltou, as tr\u00eas cores apagam. Recoloque o fio e voltam.",
    # s30
    "Do pin ao terra, a corrente fecha um circuito. S\u00f3 a perna comum d\u00e1 retorno \u00e0s tr\u00eas cores.",
    # s31
    "Se s\u00f3 uma cor falha, confira seu fio. Se as tr\u00eas apagam, confira o comum primeiro.",
    # s32
    "Como um canal da TV, o bot\u00e3o escolhe a cor. Cada aperto soma um ao n\u00famero mode.",
    # s33
    "S\u00e3o quatro modos, zero a tr\u00eas. Em tr\u00eas, aperte de novo. O que deve acontecer?",
    # s34
    "Volta a zero, como a TV ap\u00f3s o \u00faltimo canal. Na pr\u00e1tica, mode vira quatro e a linha seguinte, por ser maior que tr\u00eas, zera.",
    # s35
    "Diferente do controle, n\u00e3o h\u00e1 tela: mode fica na mem\u00f3ria. Imprima o valor para conferir.",
    # s36
    "Este \u00e9 color_modes completo: junta o bot\u00e3o do epis\u00f3dio quatro, setColor() e o fade do epis\u00f3dio cinco.",
    # s37
    "Na parte dois, um if por modo. else if s\u00f3 testa se os anteriores foram false. Zero \u00e9 vermelho, um \u00e9 verde, dois \u00e9 azul.",
    # s38
    "No else, modo tr\u00eas, level anda a cada oito milissegundos. Vermelho usa level; azul, duzentos e cinquenta e cinco menos level.",
    # s39
    "Pause: level em cento e vinte e oito, no meio do fade. Que cor d\u00e1?",
    # s40
    "Roxo, meio a meio. Vermelho sobe, azul desce: somam duzentos e cinquenta e cinco.",
    # s41
    "Tr\u00eas cliques: vermelho, verde, azul e fade. A cor muda na hora, mesmo durante o fade.",
    # s42
    "Pause e explique com suas palavras: por que mode volta a zero ap\u00f3s tr\u00eas? Basta uma frase.",
    # s43
    "S\u00e3o s\u00f3 quatro modos. Ap\u00f3s o \u00faltimo, o c\u00f3digo recome\u00e7a o ciclo.",
    # s44
    "Fa\u00e7a uma lanterna de camping: um bot\u00e3o escolhe apagado, branco fraco, branco forte ou vermelho piscando.",
    # s45
    "O truque: ap\u00f3s tr\u00eas segundos acesa, um clique desliga direto. Dica: guarde quando o modo mudou.",
    # s46
    "RGB s\u00e3o tr\u00eas LEDs. setColor() mistura com tr\u00eas n\u00fameros. O contador de modo faz um bot\u00e3o escolher.",
    # s47
    "A seguir, leia um potenci\u00f4metro e controle o brilho. Poste sua lanterna nos coment\u00e1rios; h\u00e1 solu\u00e7\u00e3o na aula. At\u00e9 l\u00e1!",
]

ES = [
    # s01
    "Un LED: rojo, verde, azul. Un toque inicia el cambio lento de azul a rojo.",
    # s02
    "Mezcla tus colores y el\u00edgelos con un bot\u00f3n.",
    # s03
    "Dos preguntas: \u00bfqu\u00e9 hace analogWrite() con ciento veintiocho en un LED?",
    # s04
    "Enciende medio ciclo, muy r\u00e1pido: ves brillo medio, pero el pin nunca est\u00e1 a medias.",
    # s05
    "Sin delay, \u00bfpor qu\u00e9 funciona siempre el bot\u00f3n?",
    # s06
    "No espera: mira el reloj, act\u00faa cuando toca y lee el bot\u00f3n en cada vuelta.",
    # s07
    "Usa el circuito cinco, un RGB, tres resistencias de doscientos veinte ohms y cables.",
    # s08
    "En el celular, mira los puntos rojos, verdes y azules: cada color de la pantalla sale de ellos.",
    # s09
    "Un RGB re\u00fane tres LEDs, rojo, verde y azul, con la pata m\u00e1s larga en com\u00fan. Es la idea de la pantalla.",
    # s10
    "La luz suma: rojo y verde dan amarillo; los tres, blanco. Con pintura, rojo y verde dan caf\u00e9.",
    # s11
    "Quita USB y LED verde de la protoboard superior: usaremos GPIO veinticinco.",
    # s12
    "Coloca la pata larga segunda desde la izquierda y \u00fanela al negativo con cable negro.",
    # s13
    "Un resistor por color: D veinticinco rojo, veintis\u00e9is verde y veintisiete azul.",
    # s14
    "\u00bfPor qu\u00e9 tres resistencias y no una com\u00fan?",
    # s15
    "Cada LED tiene su corriente. Compartir resistor es beber tres de un popote: quien jala m\u00e1s toma m\u00e1s.",
    # s16
    "Las corrientes compiten y alteran la mezcla. A diferencia del popote, gana el rojo: pide menos voltaje.",
    # s17
    "En c\u00e1todo com\u00fan, la pata larga va a tierra; para \u00e1nodo com\u00fan, cambia una l\u00ednea del c\u00f3digo.",
    # s18
    "La funci\u00f3n setColor() elige el color. Como un bot\u00f3n de cafetera, combina la dosis de tres ingredientes.",
    # s19
    "Tres analogWrite(), uno por pin, usan valores de cero a doscientos cincuenta y cinco.",
    # s20
    "A diferencia de la cafetera, da las tres dosis cada vez: no guarda recetas.",
    # s21
    "Rojo y azul a doscientos cincuenta y cinco, verde a cero: \u00bfqu\u00e9 color da?",
    # s22
    "Magenta: morado rosado. Rojo al m\u00e1ximo y cuarenta de verde dan naranja.",
    # s23
    "rgb_colors nombra tres pines. COMMON_ANODE vale false en casi todos los kits.",
    # s24
    "setColor() recibe tres valores. En \u00e1nodo com\u00fan los invierte: el m\u00e1ximo apaga.",
    # s25
    "Lee rojo, verde, azul. Pausa: cuarta l\u00ednea, dos veces doscientos cincuenta y cinco y cero. \u00bfQu\u00e9 color da?",
    # s26
    "Rojo y verde al m\u00e1ximo: amarillo. Cada segundo cambia; tras naranja, repite.",
    # s27
    "Rojo, verde, azul, amarillo, magenta, cian, blanco y naranja.",
    # s27b
    "Amarillo algo verde, magenta algo azul: el brillo no es igual. Baja verde y azul para equilibrar.",
    # s28
    "\u00bfQu\u00e9 pasa si se suelta el cable negro?",
    # s29
    "Se apagan todos los colores. Reconecta el cable y vuelven.",
    # s30
    "Del pin, la corriente vuelve a tierra. La pata com\u00fan es el \u00fanico regreso de las tres.",
    # s31
    "Si falla un color, mira su cable. Si fallan todos, mira primero el com\u00fan.",
    # s32
    "Como un canal de TV, el bot\u00f3n elige el color. Cada pulsaci\u00f3n suma uno al n\u00famero mode.",
    # s33
    "Hay cuatro modos, cero a tres. En tres, pulsa otra vez. \u00bfQu\u00e9 debe pasar?",
    # s34
    "Vuelve a cero, como tras el \u00faltimo canal. mode vale cuatro; la siguiente l\u00ednea ve que supera tres y lo pone en cero.",
    # s35
    "A diferencia del control, no hay pantalla: mode vive en memoria. Imprime el valor para revisarlo.",
    # s36
    "Este es color_modes completo: junta el bot\u00f3n del episodio cuatro, setColor() y el fade del episodio cinco.",
    # s37
    "Hay un if por modo. else if solo se prueba si los anteriores fueron false. Cero es rojo, uno verde y dos azul.",
    # s38
    "En el else, modo tres, level avanza cada ocho milisegundos. Rojo usa level; azul, doscientos cincuenta y cinco menos level.",
    # s39
    "Pausa: level en ciento veintiocho, a mitad del fade. \u00bfQu\u00e9 color ves?",
    # s40
    "Morado: mitad rojo y azul. Uno sube, otro baja: suman doscientos cincuenta y cinco.",
    # s41
    "Tres pulsaciones: rojo, verde, azul y fade. La respuesta es inmediata, incluso durante el fade.",
    # s42
    "Pausa y explica con tus palabras: \u00bfpor qu\u00e9 mode vuelve a cero tras tres? Basta una frase.",
    # s43
    "Solo hay cuatro modos. Tras el \u00faltimo, el c\u00f3digo reinicia el ciclo.",
    # s44
    "Haz una linterna de camping: el bot\u00f3n elige apagado, blanco tenue, blanco fuerte o rojo parpadeante.",
    # s45
    "El truco: tras tres segundos encendida, una pulsaci\u00f3n la apaga. Pista: guarda cu\u00e1ndo cambi\u00f3 el modo.",
    # s46
    "RGB re\u00fane tres LEDs; setColor() mezcla con tres n\u00fameros; un contador deja al bot\u00f3n elegir.",
    # s47
    "Luego leeremos un potenci\u00f3metro para ajustar brillo. Comenta tu linterna; hay soluci\u00f3n en la carpeta. \u00a1Nos vemos!",
]

TARGET = {"hi": 1.05, "pt": 1.00, "es": 1.00}


def check(langs, english):
    """Print per-language max/mean char ratio vs the English narration; return the over-target lines."""
    over = []
    for lang, seg in langs.items():
        ratios = {k: len(seg[k]) / len(english[k]) for k in english}
        worst = max(ratios, key=ratios.get)
        print(f"{lang}: max {ratios[worst]:.2f} ({worst}), mean {sum(ratios.values()) / len(ratios):.2f}, target <= {TARGET[lang]:.2f}")
        over += [(lang, k, r) for k, r in ratios.items() if r > TARGET[lang] + 1e-9]
    for lang, k, r in over:
        print(f"  OVER {lang} {k}: {r:.2f} ({len(langs[lang][k])} vs {len(english[k])} chars)")
    return over


if __name__ == "__main__":
    script = json.loads((ROOT / "script.json").read_text(encoding="utf-8"))
    english = {s["id"]: s["text"] for s in script["segments"]}
    out = ROOT / "dub"
    out.mkdir(exist_ok=True)
    langs = {}
    for lang, voice, lines in (("hi", "hi-IN-MadhurNeural", HI), ("pt", "pt-BR-AntonioNeural", PT), ("es", "es-MX-JorgeNeural", ES)):
        assert len(lines) == len(IDS) == 48, (lang, len(lines), len(IDS))
        seg = dict(zip(IDS, lines))
        langs[lang] = seg
        (out / f"{lang}.json").write_text(json.dumps({"voice": voice, "rate": "+0%", "segments": seg}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("dubs written:", ", ".join(langs))
    check(langs, english)
