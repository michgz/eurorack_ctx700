PYTHON = python

all: output/euro.midiox

clean:
	$(RM) output/euro.midiox

output/euro.midiox: scripts/makemidi.py
	$(PYTHON) scripts/makemidi.py output/euro.midiox

.PHONY: all
