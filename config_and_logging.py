import ConfigParser

def read_section_with_defaults(config, section, defaults):
  filled = {}
  options = config.options(section)
  for key in options:
    filled[key] = config.get(section, key)
  for key in defaults:
    if key not in options:
      filled[key] = defaults[key]
  return filled

def read_config():
  config = ConfigParser.ConfigParser()
  config.read("rats_config.ini")
  defaults = {"filename":"rats.MTS", "outfile": "output.csv", "logfile":"rats_log.txt", "first_rat_frame": 343, "stable_camera_frame": 200, "rearing_line":600, "mid_line":700, "show_debug": True}
  configured = read_section_with_defaults(config, "Video", defaults)
  print "Read these config values:"
  print configured
  return configured
