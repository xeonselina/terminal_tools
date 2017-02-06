import os
import pexpect

p = pexpect.popen_spawn.PopenSpawn('cmd')

p.interact()

