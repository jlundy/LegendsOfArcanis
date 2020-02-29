#!/usr/bin/python3
import argparse
import sys
import yaml
import textwrap
from string import Template

def parse_arguments():
  argParse = argparse.ArgumentParser()
  argParse.add_argument("-s", "--speed", help="REQUIRED: The speed of your weapon", type=int, required=True)
  argParse.add_argument("-i", "--input", help="OPTIONAL: The YML file containing your spells.  Defaults to 'spells.yml'", default="spells.yml")
  argParse.add_argument("-o", "--output", help="OPTIONAL:  The output file containing the Arcane Strike maneuvers. \
    Defaults to 'arcane_strike.out'", default="arcane_strike.out") 
  argParse.add_argument("-r", "--readable", help="OPTIONAL:  Create a file for importing into the maneuver calculator", default=False, action="store_true") 
  args = argParse.parse_args()
  return args

arguments = parse_arguments()
weaponSpeed = arguments.speed
humanReadable = arguments.readable

with open(arguments.input, 'r') as inputFile:
  spell_data = inputFile.read()

# parse the yml file here
spells = yaml.full_load(spell_data)

with open(arguments.output, 'w') as outputFile:
  for spell in spells.items():
    maneuver_name = "Arcane Strike(%s)" % spell[0]
    maneuver_speed = max(weaponSpeed, spell[1]['Speed'])
    recovery = min(weaponSpeed, spell[1]['Speed'])
    strain = spell[1]['Strain']
    description = spell[1]['Description']
    ctn = spell[1]['CTN']

    # Need to implement manevuer output file later
    header_data = Template("$maneuver_name\n  Speed(Recovery/Strain): $maneuver_speed($recovery, $strain)\n  CTN: $ctn\n").safe_substitute\
      (maneuver_name=maneuver_name, maneuver_speed=maneuver_speed, recovery=recovery, strain=strain, ctn=ctn)
    description_data = textwrap.wrap(description, 50, break_long_words=False)
    
    outputFile.write(header_data)
    for lines in description_data:
      outputFile.write("  ")
      outputFile.write(lines)
      outputFile.write("\n")
    outputFile.write("\n\n")
   
