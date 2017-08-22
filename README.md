# About PatchBook:

PatchBook is a markup language and parser for writing and distributing patches for modular synthesizers created by [Spektro Audio](http://spektroaudio.com/).
The markup language is designed to be easily readable and writeable by humans while the parser can process .txt files written in the PatchBook format and output a JSON file that can be used by other applications to display and process the patch's data.

**Patchbook Version:** 1.0  
**Parser version:** b1

**Table of Content:**

<!-- MarkdownTOC -->

- Markup Description
	- Voices
	- Connections
	- Parameters
	- Examples
- Parser
	- Requirements
	- How to Use
	- Data Structure

<!-- /MarkdownTOC -->


---

# Markup Description

---

## Voices

**Voices** must be written in all caps, without any spaces before the name and followed by a colon.  
Examples:

- BASS 1:
- VOICE 1:
- LEAD:

Every connection described after a voice anotation will be assigned to that voice.

---

## Connections

Every connection (patch cable) must be annotated using the following format: **- Output Module (Output Label) >> Input Module (Input Label)**.  
Examples:  

- Maths (Ch. 1 Unity) >> Polaris (CV 2)
- Tides (Bi) >> Braids (Timbre)

While the >> indicator can be used to indicate a standard connection, it could (and should) also be replaced by more specific indicators according to the kind of signal being sent from the Output Module to the Input Module:  

- \>> for CV
- -> for Audio
- p> for Pitch (1v/oct or Hz/V)
- g> for Gate
- t> for Trigger
- c> for Clock

Examples:

- Metropolis (Pitch) p> Braids (1 V/Oct)
- Pamela's Workout (1) c> Penta (Clk)
- Braids (Out) -> Polaris (Input)

**Additional info:**

- The manufacture's name should only be included if the module's name is too generic (example: VB Modular ADSR).
- Non-modular equipment (such as audio interfaces, recorders, and other synths) should be written in all caps: NAME OF GEAR (Input or Output).

---

## Parameters

Parameters can be annotated in 2 different ways: single line or multiline. Every parameter annotation must start with an asterisk character before the module name.

**Single-line**  
\* Function: Rise = 50% | Fall = 50% | Curve = 30%

**Multi-Line**  
\* Braids:  
	| Mode = CSAW  
	| Color = 50%  
	| Timbre = 50%  
	
**Additional info**

- Parameter values can be written as knob / fader position (percentage), specific value followed by unit (5Hz, 10ms, etc), or as a descriptive value (fast, slow, simple, complex, short, long).
- Parameters are not assigned to any voice since the same module can be used in multiple voices. 
 

---

## Examples

---

### Example 1

```
VOICE 1:
	- Metropolis (Pitch) p> Braids (1v/oct)
	- Metropolis (Gate) g> Function (Trigger)
	- Braids (Out) -> Optomix (Ch1 Signal)
	- Function (+ Out) >> Optomix (Ch1 CV)
	- Function (- Out) >> Braids (Timbre CV)
	- Optomix (Out 1) -> AUDIO INTERFACE (input)
	
	* Metropolis:
	| BPM = 124
	| Swing = 0
	| Root = F
	| Scale = Minor
	| Mode = F. Forward
	| Stages = 16
	
	* Braids:
	| Mode = Fold
	| Timbre = 30%
	| Timbre CV = -20%
	| Color = 0%

	* Function: Rise = 50% | Fall = 50% | Curve = 30%
	* Optomix: Damp = 0% | Control = 100%
```

### Example 2

```
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

```

----

# Parser

The PatchBook parser is a Python program that can read text files written in the PatchBook format and generate a JSON file.

---
## Requirements

-  Python 3

---
## How to Use

To use the parser, download the python script, open the terminal and use the command:

```python3 path/to/script/patchbook.py -file /path/to/textfile.txt```

After loading the text file into the parser, you can use the following commands to process it:

-	**module**: Outputs a list of connections and parameters for a specific module.
- **connections**: Prints a list of all connections organized by type (pitch, gate, clock, etc).
- **export**: Generates a JSON file based on the input text file.
- **mermaid**: Generates a code that can be copied to pasted into the [Mermaid Live Editor](https://mermaidjs.github.io/mermaid-live-editor/) to generate a signal flow chart for the patch (that can be downloaded as an SVG file).
![Example 1 signal flow generated using Mermaid](/Images/mermaid-signal-flow.png?raw=true)

------
## Data Structure

![Patchbook Data Structure](/Images/datastructure.png?raw=true)

-----

Patchbook was created by Ícaro Ferre / Spektro Audio.  
Twitter: @icaroferre / @spektroaudio  
http://spektroaudio.com/  

