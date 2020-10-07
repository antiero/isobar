#!/usr/bin/env python3

#------------------------------------------------------------------------
# isobar: ex-basics
# 
# Example of some basic functionality: Pattern transformations,
# sequences, scales, stochastic functions, scheduling and mapping.
#------------------------------------------------------------------------

import isobar as iso

#------------------------------------------------------------------------
# Turn on some basic logging output. 
#------------------------------------------------------------------------
import logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")

#------------------------------------------------------------------------
# Create a geometric series on a minor scale.
# PingPong plays the series forward then backward. PLoop loops forever.
#------------------------------------------------------------------------
arpeggio = iso.PSeries(0, 2, 6)
arpeggio = iso.PDegree(arpeggio, iso.Scale.minor) + 72
arpeggio = iso.PPingPong(arpeggio)
arpeggio = iso.PLoop(arpeggio)

#------------------------------------------------------------------------
# Create a velocity sequence, with emphasis every 4th note,
# plus a random walk to create gradual dynamic changes.
# Amplitudes are in the MIDI velocity range (0..127).
#------------------------------------------------------------------------
amplitude = iso.PSequence([50, 35, 25, 35]) + iso.PBrown(0, 1, -20, 20)

#------------------------------------------------------------------------
# Create a repeating sequence with scalar transposition:
# [ 36, 38, 43, 39, 36, 38, 43, 39, ... ]
#------------------------------------------------------------------------
bassline = iso.PSequence([0, 2, 7, 3]) + 36

#------------------------------------------------------------------------
# Repeat each note 3 times, and transpose each into a different octave
# [ 36, 48, 60, 38, 50, 62, ... ]
#------------------------------------------------------------------------
bassline = iso.PStutter(bassline, 3) + iso.PSequence([0, 12, 24])

#------------------------------------------------------------------------
# A Timeline schedules events at a specified tempo. By default, events
# are send to the system's default MIDI output.
#------------------------------------------------------------------------
output = iso.MidiOutputDevice()

timeline = iso.Timeline(120, output)

#------------------------------------------------------------------------
# Schedule events, with properties generated by the Pattern objects.
#------------------------------------------------------------------------
timeline.schedule({
    "note": arpeggio,
    "duration": 0.25,
    "amplitude": amplitude
})
timeline.schedule({
    "note": bassline,
    "duration": 1
})

timeline.run()
