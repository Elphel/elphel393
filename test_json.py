import json

with open('projects.json') as data_file:
    Projects = json.load(data_file)

for p,v in Projects.items():
    print("    "+p+":")
    if isinstance(v,dict):
      for k,l in v.items():
          print("        "+k+":")
          tmpstr = "        "
          for e in l:
            if e=="": 
              e = "\"\""
            tmpstr += "    "+e
          print(tmpstr)
    elif isinstance(v,list):
      tmpstr = "    "
      for e in v:
        tmpstr += "    "+e
      print(tmpstr)

print("\n0 errors\n")