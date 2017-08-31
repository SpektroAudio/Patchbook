"""
PATCHBOOK MARKUP LANGUAGE & PARSER
CREATED BY SPEKTRO AUDIO
http://spektroaudio.com/
"""

import sys
import re
import os
import argparse
import json

# Parser INFO
parserVersion = "b3"

# Reset main dictionary
mainDict = {
    "info": {"patchbook_version": parserVersion},
    "modules": {},
    "comments": []
}

# Available connection types
connectionTypes = {
    "->": "audio",
    ">>": "cv",
    "p>": "pitch",
    "g>": "gate",
    "t>": "trigger",
    "c>": "clock"
}


# Reset global variables
lastModuleProcessed = ""
lastVoiceProcessed = ""

# Parse script arguments
parser = argparse.ArgumentParser()
parser.add_argument("-file", type=str, default="",
                    help="Name of the text file that will be parsed (including extension)")
parser.add_argument("-debug", type=int, default=0,
                    help="Enable Debugging Mode")
args = parser.parse_args()
filename = args.file
debugMode = args.debug
connectionID = 0

# Set up debugMode
if args.debug == 1:
    debugMode = True
else:
    debugMode = False


def initial_print():
    print()
    print("██████████████████████████████")
    print("       PATCHBOOK PARSER       ")
    print("   Created by Spektro Audio   ")
    print("██████████████████████████████")
    print()
    print("Version " + parserVersion)
    print()


def get_script_path():
    # Get path to python script
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def getFilePath(filename):
    try:
        # Append script path to the filename
        base_dir = get_script_path()
        filepath = os.path.join(base_dir, filename)
        if debugMode:
            print("File path: " + filepath)
        return filepath
    except IndexError:
        pass


def parseFile(filename):
    # This function reads the txt file and process each line.
    lines = []
    try:
        print("Loading file: " + filename)
        with open(filename, "r") as file:
            for l in file:
                lines.append(l)
                regexLine(l)
    except TypeError:
        print("ERROR. Please add text file path after the script.")
    except FileNotFoundError:
        print("ERROR. File not found.")
    print("File successfully processed.")
    print()


def regexLine(line):
    global lastModuleProcessed
    global lastVoiceProcessed

    if debugMode:
        print()
    if debugMode:
        print("Processing: " + line)

    # CHECK FOR COMMENTS
    if debugMode:
        print("Checking input for comments...")
    re_filter = re.compile(r"^\/\/\s(.+)$")  # Regex for "// Comments"
    re_results = re_filter.search(line.strip())
    try:
        comment = re_results.group().replace("//", "").strip()
        if debugMode:
            print("New comment found: " + comment)
            addComment(comment)
        return
    except AttributeError:
        pass

    # CHECK FOR VOICES
    if debugMode:
        print("Cheking input for voices...")
    re_filter = re.compile(r"^(.+)\:$")  # Regex for "VOICE 1:"
    re_results = re_filter.search(line)
    try:
        # For some reason the Regex filter was still detecting parameter declarations as voices,
        # so I'm also running the results through an if statement.
        results = re_results.group().replace(":", "")
        if "*" not in results and "-" not in results and "|" not in results:
            if debugMode:
                print("New voice found: " + results.upper())
            lastVoiceProcessed = results.upper()
            return
    except AttributeError:
        pass

    # CHECK FOR CONNECTIONS
    if debugMode:
        print("Cheking input for connections...")
    re_filter = re.compile(
        r"\-\s(.+)[(](.+)[)]\s(\>\>|\-\>|[a-z]\>)\s(.+)[(](.+)[)]\s(\[.+\])?$")
    re_results = re_filter.search(line)
    try:
        results = re_results.groups()
        voice = lastVoiceProcessed
        if len(results) == 6:
            if debugMode:
                print("New connection found, parsing info...")
            # args = parseArguments(results[5])
            # results = results[:5]
            addConnection(results, voice)
            return
    except AttributeError:
        pass

    # CHECK PARAMETERS
    if debugMode:
        print("Checking for parameters...")
    # If single-line parameter declaration:
    re_filter = re.compile(r"^\*\s(.+)\:\s?(.+)?$")
    re_results = re_filter.search(line.strip())
    try:
        # Get module name
        results = re_results.groups()
        module = results[0].strip().lower()
        if debugMode:
            print("New module found: " + module)
        if results[1] != None:
            # If parameters are also declared
            parameters = results[1].split(" | ")
            for p in parameters:
                p = p.split(" = ")
                addParameter(module, p[0].strip().lower(), p[1].strip())
            return
        elif results[1] == None:
            if debugMode:
                print("No parameters found. Storing module as global variable...")
            lastModuleProcessed = module
            return
    except AttributeError:
        pass

    # If multi-line parameter declaration:
    if "|" in line and "=" in line and "*" not in line:
        module = lastModuleProcessed.lower()
        if debugMode:
            print("Using global variable: " + module)
        parameter = line.split(" = ")[0].replace("|", "").strip().lower()
        value = line.split(" = ")[1].strip()
        addParameter(module, parameter, value)
        return


def parseArguments(args):
    # This method takes an arguments string like "[color = blue]" and converts it to a dictionary
    args_string = args.replace("[", "").replace("]", "")
    args_array = args_string.split(",")
    args_dict = {}

    if debugMode:
        print("Parsing arguments: " + args)

    for item in args_array:
        item = item.split("=")
        name = item[0].strip()
        value = item[1].strip()
        args_dict[name] = value
        if debugMode:
            print(name + " = " + value)

    if debugMode:
        print("All arguments processes.")

    return args_dict


def addConnection(list, voice="none"):
    global mainDict
    global connectionTypes
    global connectionID

    connectionID += 1

    if debugMode:
        print("Adding new connection...")
    if debugMode:
        print("-----")

    output_module = list[0].lower().strip()
    output_port = list[1].lower().strip()

    if debugMode:
        print("Output module: " + output_module)
    if debugMode:
        print("Output port: " + output_port)

    try:
        connection_type = connectionTypes[list[2].lower()]
        if debugMode:
            print("Matched connection type: " + connection_type)
    except KeyError:
        print("Invalid connection: " + list[2])
        connection_type = "cv"

    input_module = list[3].lower().strip()
    input_port = list[4].lower().strip()

    if list[5] is not None:
        arguments = parseArguments(list[5])
    else:
        arguments = {}

    if debugMode:
        print("Input module: " + input_module)
    if debugMode:
        print("Input port: " + output_port)

    checkModuleExistance(output_module, output_port, "out")
    checkModuleExistance(input_module, input_port, "in")

    if debugMode:
        print("Appending output and input connections to mainDict...")

    output_dict = {
        "input_module": input_module,
        "input_port": input_port,
        "connection_type": connection_type,
        "voice": voice,
        "id": connectionID}

    input_dict = {
        "output_module": output_module,
        "output_port": output_port,
        "connection_type": connection_type,
        "voice": voice,
        "id": connectionID}

    for key in arguments:
        output_dict[key] = arguments[key]
        input_dict[key] = arguments[key]

    mainDict["modules"][output_module]["connections"]["out"][output_port].append(
        output_dict)
    mainDict["modules"][input_module]["connections"]["in"][input_port] = input_dict
    if debugMode:
        print("-----")


def checkModuleExistance(module, port="port", direction=""):
    global mainDict

    if debugMode:
        print("Checking if module already existing in main dictionary: " + module)

    # Check if module exists in main dictionary
    if module not in mainDict["modules"]:
        mainDict["modules"][module] = {
            "parameters": {},
            "connections": {"out": {}, "in": {}}
        }

    # If it exists, check if the port exists
    if direction == "in":
        if port not in mainDict["modules"][module]["connections"]["in"]:
            mainDict["modules"][module]["connections"]["in"][port] = []

    if direction == "out":
        if port not in mainDict["modules"][module]["connections"]["out"]:
            mainDict["modules"][module]["connections"]["out"][port] = []


def addParameter(module, name, value):
    checkModuleExistance(module)
    # Add parameter to mainDict
    if debugMode:
        print("Adding parameter: " + module + " - " + name + " - " + value)
    mainDict["modules"][module]["parameters"][name] = value


def addComment(value):
    mainDict["comments"].append(value)


def askCommand():
    command = input("> ").lower().strip()
    if command == "module":
        detailModule()
    elif command == "print":
        printDict()
    elif command == "export":
        exportJSON()
    elif command == "connections":
        printConnections()
    elif command == "graph":
        graphviz()
    else:
        print("Invalid command, please try again.")
    askCommand()


def detailModule():
    global mainDict
    module = input("Enter module name: ").lower()
    if module in mainDict["modules"]:
        print("-------")
        print("Showing information for module: " + module.upper())
        print()
        print("Inputs:")
        for c in mainDict["modules"][module]["connections"]["in"]:
            keyvalue = mainDict["modules"][module]["connections"]["in"][c]
            print(keyvalue["output_module"].title() + " (" + keyvalue["output_port"].title(
            ) + ") > " + c.title() + " - " + keyvalue["connection_type"].title())
        print()

        print("Outputs:")
        for x in mainDict["modules"][module]["connections"]["out"]:
            port = mainDict["modules"][module]["connections"]["out"][x]
            for c in port:
                keyvalue = c
                print(x.title() + " > " + keyvalue["input_module"].title() + " (" + keyvalue["input_port"].title(
                ) + ") " + " - " + keyvalue["connection_type"].title() + " - " + keyvalue["voice"])
        print()

        print("Parameters:")
        for p in mainDict["modules"][module]["parameters"]:
            value = mainDict["modules"][module]["parameters"][p]
            print(p.title() + " = " + value)
        print()

        print("-------")


def printConnections():
    print()
    print("Printing all connections by type...")
    print()

    for ctype in connectionTypes:
        ctype_name = connectionTypes[ctype]
        print("Connection type: " + ctype_name)
        # For each module
        for module in mainDict["modules"]:
            # Get all outgoing connections:
            connections = mainDict["modules"][module]["connections"]["out"]
            for c in connections:
                connection = connections[c]
                for subc in connection:
                    # print(connection)
                    if subc["connection_type"] == ctype_name:
                        print(module.title(
                        ) + " > " + subc["input_module"].title() + " (" + subc["input_port"].title() + ") ")
        print()


def exportJSON():
    # Exports mainDict as json file
    name = filename.split(".")[0]
    filepath = getFilePath(name + '.json')
    print("Exporting dictionary as file: " + filepath)
    with open(filepath, 'w') as fp:
        json.dump(mainDict, fp)


def graphviz():
    linetypes = {
        "audio": {"style": "bold"},
        "cv": {"color": "gray"},
        "gate": {"color": "red", "style": "dashed"},
        "trigger": {"color": "orange", "style": "dashed"},
        "pitch": {"color": "blue"},
        "clock": {"color": "purple", "style": "dashed"}
    }
    print("Generating signal flow code for GraphViz.")
    print("Copy the code between the line break and paste it into https://dreampuf.github.io/GraphvizOnline/ to download a SVG / PNG chart.")
    conn = []
    total_string = ""
    print("-------------------------")
    print("digraph G{\nrankdir = LR;\nsplines = polyline;\nordering=out;")
    total_string += "digraph G{\nrankdir = LR;\nsplines = polyline;\nordering=out;\n"
    for module in sorted(mainDict["modules"]):
        # Get all outgoing connections:
        outputs = mainDict["modules"][module]["connections"]["out"]
        module_outputs = ""
        out_count = 0
        for out in sorted(outputs):
            out_count += 1
            out_formatted = "_" + re.sub('[^A-Za-z0-9]+', '', out)
            module_outputs += "<" + out_formatted + "> " + out.upper()
            if out_count < len(outputs.keys()):
                module_outputs += " | "
            connections = outputs[out]
            for c in connections:
                line_style_array = []
                graphviz_parameters = [
                    "color", "weight", "style", "arrowtail", "dir"]
                for param in graphviz_parameters:
                    if param in c:
                        line_style_array.append(param + "=" + c[param])
                    elif param in linetypes[c["connection_type"]]:
                        line_style_array.append(
                            param + "=" + linetypes[c["connection_type"]][param])
                if len(line_style_array) > 0:
                    line_style = "[" + ', '.join(line_style_array) + "]"
                else:
                    line_style = ""
                in_formatted = "_" + \
                    re.sub('[^A-Za-z0-9]+', '', c["input_port"])
                connection_line = module.replace(" ", "") + ":" + out_formatted + ":e  -> " + \
                    c["input_module"].replace(
                        " ", "") + ":" + in_formatted + ":w " + line_style
                conn.append([c["input_port"], connection_line])

        # Get all incoming connections:
        inputs = mainDict["modules"][module]["connections"]["in"]
        module_inputs = ""
        in_count = 0
        for inp in sorted(inputs):
            inp_formatted = "_" + re.sub('[^A-Za-z0-9]+', '', inp)
            in_count += 1
            module_inputs += "<" + inp_formatted + "> " + inp.upper()
            if in_count < len(inputs.keys()):
                module_inputs += " | "

        # Get all parameters:
        params = mainDict["modules"][module]["parameters"]
        module_params = ""
        param_count = 0
        for par in sorted(params):
            param_count += 1
            module_params += par.title() + " = " + params[par]
            if param_count < len(params.keys()):
                module_params += r'\n'

        # If module contains parameters
        if module_params != "":
            # Add them below module name
            middle = "{{" + module.upper() + "}|{" + module_params + "}}"
        else:
            # Otherwise just display module name
            middle = module.upper()

        final_box = module.replace(
            " ", "") + "[label=\"{ {" + module_inputs + "}|" + middle + "| {" + module_outputs + "}}\"  shape=Mrecord]"
        print(final_box)
        total_string += final_box + "; "

    # Print Connections
    for c in sorted(conn):
        print(c[1])
        total_string += c[1] + "; "

    if len(mainDict["comments"]) != 0:
        format_comments = ""
        comments_count = 0
        for comment in mainDict["comments"]:
            comments_count += 1
            format_comments += "{" + comment + "}"
            if comments_count < len(mainDict["comments"]):
                format_comments += "|"
        format_comments = "comments[label=<{{{<b>PATCH COMMENTS</b>}|" + format_comments + "}}>  shape=Mrecord]"
        print(format_comments)

    print("}")
    total_string += "}"

    print("-------------------------")
    print()
    return total_string


def printDict():
    global mainDict
    for key in mainDict["modules"]:
        print(key.title() + ": " + str(mainDict["modules"][key]))


if __name__ == "__main__":
    initial_print()
    parseFile(filename)
    askCommand()
