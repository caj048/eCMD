#!/usr/bin/env python

import os
import errno

# A script to create the files generated by the configured extensions
# Configured extensions come from the EXTENSIONS environment variable

# Create the ecmdExtInterpreter.C
# This is a combo of generated code from this script and code snippets
# stored with the extension

# Get the list of extensions from the env and turn it into python
extlist = os.environ["EXTENSIONS"].split(" ")
extlist.sort()

# Go thru the full extlist and create a reduced list of extensions
# with no cmd component
extcmdlist = list()
for ext in extlist:
  if (os.path.exists(os.environ["ECMD_ROOT"] + "/ext/" + ext + "/cmd/snippet")):
      extcmdlist.append(ext)

# Create the generated src directory
srcdir = os.environ["ECMD_ROOT"] + "/cmd/" + os.environ["SRCDIR"]
if (not os.path.exists(srcdir)):
  os.makedirs(srcdir)

# Open our file and start writing
extfile = open(os.environ["ECMD_ROOT"] + "/cmd/" + os.environ["SRCDIR"] + "/ecmdExtInterpreter.C", 'w')

# Write out all the static stuff
extfile.write("//This file was autogenerated by makeext.py\n\n")
extfile.write("#include <inttypes.h>\n")
extfile.write("#include <dlfcn.h>\n")
extfile.write("#include <stdio.h>\n")
extfile.write("#include <string.h>\n")
extfile.write("\n")
extfile.write("#include <ecmdClientCapi.H>\n")
extfile.write("#include <ecmdExtInterpreter.H>\n")
extfile.write("#include <ecmdReturnCodes.H>\n")
extfile.write("#include <ecmdCommandUtils.H>\n")
extfile.write("#include <ecmdSharedUtils.H>\n\n")

# Now loop through all the extensions and write out their defines and includes
for ext in extcmdlist:
  extfile.write("#ifdef ECMD_" + ext.upper() + "_EXTENSION_SUPPORT\n")
  extfile.write("#include <" + ext + "ClientCapi.H>\n")
  extfile.write("#include <" + ext + "Interpreter.H>\n")
  extfile.write("#endif\n\n")

# Write the function definition
extfile.write("uint32_t ecmdCallExtInterpreters(int argc, char* argv[], uint32_t & io_rc) {\n")
extfile.write("  uint32_t rc = ECMD_SUCCESS;\n\n")

# Now go through and suck in all the extension init code snippets
# Once read in, place it in the new output file
for ext in extcmdlist:
  snippetfile = open(os.environ["ECMD_ROOT"] + "/ext/" + ext + "/cmd/snippet/callInterpreter.C", 'r')
  for line in snippetfile.readlines():
    extfile.write(line)
  extfile.write("\n")
  snippetfile.close()	

# Write the end of the function and close the file
extfile.write("  return rc;\n")
extfile.write("}\n")
extfile.close()
