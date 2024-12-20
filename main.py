import axinite.tools as axtools
import sys

if sys.argv[1] == "load":
    args = axtools.read(sys.argv[2])
    axtools.load(args, sys.argv[3])
if sys.argv[1] == "show":
    args = axtools.read(sys.argv[2])
    axtools.show(args, axtools.plotly_frontend(args, "show"))
if sys.argv[1] == "live":
    args = axtools.read(sys.argv[2])
    axtools.live(args, axtools.vpython_frontend(args, "live"))
if sys.argv[1] == "run":
    args = axtools.read(sys.argv[2])
    axtools.run(args, axtools.vpython_frontend(args, "run"))