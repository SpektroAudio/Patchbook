VOICE 1:

	- Metropolis (Pitch) p> Aether VCO (CV)
	- Metropolis (Gate) g> Maths (Ch 1 Trigger)
	- Metropolis (Gate) g> Maths (Ch 4 Trigger)
	
	* Aether VCO: LFO Freq = 5 | LFO PWM = 7
	- Aether VCO (Pulse) -> Mixer (Ch1)
	- Aether VCO (Sub 1) -> Tides (Clk)
	- Tides (Bi) -> Mixer (Ch2)
	- Aether VCO (Sub 2) -> Z3000 (HSync)
	- Z3000 (Saw) -> Mixer (Ch3)
	
	- MultiLFO (LFO 1) >> Tides (Smoothness)
	- MultiLFO (LFO 2 Triangle) >> Tides (Shape)
	- MultiLFO (LFO 3 Triangle) >> Z3000 (PWM)
	* MultiLFO:
	| LFO 1 Freq = 3.8
	| LFO 1 Shape = Sine
	| LFO 1 S&H = 0
	| LFO 2 Freq = 1
	| LFO 3 Freq = 1
	* Tides: PLL Mode = True | Freq = 60% | Smoothness = 70%
	* Z3000: Freq = 1pm
	
	- Maths (Ch 1) >> Multifilter (CV)
	- Maths (Ch 4) >> uVCA (Ch1 CV)
	
	- Mixer (Output) -> Multifilter (Input)
	- Multifilter (LPF) -> uVCA (Ch1 Input)
	- uVCA (Ch1 Output) -> AUDIO INTERFACE (In 3)

	