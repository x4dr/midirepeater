import rtmidi
import time

midiin = rtmidi.MidiIn()
midiout = rtmidi.MidiOut()

for i, name in enumerate(midiin.get_ports()): # autoselect first found usb midi device
    if "USB" in name:
        midiin.open_port(i)
        midiout.open_port(i)
        break
else:
    raise IOError("No USB midi device detected")


def callback(event, data=None):
    message, deltatime = event
    status = message[0]

    if (status & 0xF0) == 0xC0: # left byte should be C for song select
        channel = status & 0x0F # right byte is channel
        prog = message[1] # right part of message is song

        #  beat buddy needs banks selected before song select
        midiout.send_message([0xB0 | channel, 0x00, 0x00])  # CC 0 (Bank MSB)
        midiout.send_message([0xB0 | channel, 0x20, 0x00])  # CC 32 (Bank LSB)
        midiout.send_message([0xC0 | channel, prog])
    else: #send everything that isn't handled through
        midiout.send_message(message)

midiin.set_callback(callback)
midiin.ignore_types(sysex=False, timing=False, active_sense=False) # send timing, sysex and active sense through
print("repeating midi input Ctrl-C to quit.")

while True:
    time.sleep(1) # wait forever while repeating
