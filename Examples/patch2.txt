VOICE 1:
	- Metropolis (Pitch) p> Lizard2 (CV)
	- Lizard2 (Out 2) -> Multifilter (Input)
	- Multifilter (LPF) -> Optomix (Ch1 Signal)
	- Metropolis (Pitch) p> Multifilter (1V/oct)
	- Metropolis (Gate) g> Z4000 (Gate)
	- Z4000 (Out) >> Optomix (Ch1 CV)
	- Metropolis (Gate) g> Function (Gate)
	- Function (Pos Out) >> Multifilter (CV Input)

VOICE 2:
	- Metropolis (Clock) c> SequentialVoltage (CLK In)
	- Metropolis (Reset) t> SequentialVoltage (Reset)
	- SequentialVoltage (Out) >> Braids (1V/Oct)
	- Braids (Out) -> A124 (Input)
	- e350 (XY) >> A124 (CV2)
	- MultiLFO (LFO 2) >> Braids (Timbre)