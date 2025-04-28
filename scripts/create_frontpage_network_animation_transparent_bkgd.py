#!/usr/bin/env python

# NOTE: You must install "ffmpeg" for this script to work, and "ffmpeg" is NOT a Python package!

print("""
--> If you want to produce the animation with a transparent background, currently
you need to install 'ffmpeg': ( https://ffmpeg.org/download.html ) . The
easiest way to install it is through a package manager for your system. For
example, if you are on MacOS, you may want to install Homebrew
( https://brew.sh/ ), followed by running

$ brew install ffmpeg

Running the above command will install ffmpeg into your system, after which you should re-run this script.
""")

# adapted from https://jonescompneurolab.github.io/hnn-core/stable/auto_examples/howto/plot_hnn_animation.html#sphx-glr-auto-examples-howto-plot-hnn-animation-py

from hnn_core import jones_2009_model, simulate_dipole
from hnn_core.network_models import add_erp_drives_to_jones_model
from hnn_core.viz import NetworkPlotter

import matplotlib.pyplot as plt

net = jones_2009_model(mesh_shape=(5, 5))

# Note that we move the cells further apart to allow better visualization of
# the network (default inplane_distance=1.0 µm).
net.set_cell_positions(inplane_distance=300)

add_erp_drives_to_jones_model(net)
dpl = simulate_dipole(net, tstop=170, record_vsec='all')


# Must be done before NetworkPlotter()
plt.rcParams.update({
    "savefig.facecolor": (0.0, 0.0, 0.0, 0.0)
})

# Note that this only appears to set the background color of the axes objects,
# NOT the figure entirely! For a transparent figure background in the exported
# animation file, see below.
net_plot = NetworkPlotter(net, bg_color='none')

print(net_plot._bg_color)

# Animation at 15 fps is 680 frames = 45 seconds long.
fps = 15

# However, there aren't strictly 680 frames: because frame "decimation" is 10
# by default, there are approximately 6795 frames. To make things more
# complicated, frames are accessible in numbers ending in 5 for some
# reason. So, for example, frame "795" is close to frame 800, and 800 / 10
# (decimation) / 15 fps = time of 5.33... ; in other words, frame 795 is going
# to be close to "time 5.33... seconds" of the animation.

# Since we are not interested in the initial, "quiet" part of the simulation
# before spiking really begins, we should only use a frames starting at a later
# point in time, like frame 795:
frame_start=795

# Similarly, since we want to keep the movie's file size low, and we don't need
# to show that much of the simulation itself, we will only use the frames up to
# frame 1495 (approximately "time 10 seconds" of the full animation):
frame_stop=1495

### transparent #############################################
# This makes a copy of the movie with a transparent background

try:
    # Note that we have to increase the dpi because the default settings for the
    # ffmpeg backend look much worse.
    ani = net_plot.export_movie('frontpage-network-animation-transparent-bkgd.gif',
                                dpi=300,
                                fps=fps,
                                frame_start=frame_start,
                                frame_stop=frame_stop,
                                writer='ffmpeg_file',
                                )
except RuntimeError as exc:
    print("""
    \n--> ERROR: You probably don't have 'ffmpeg' installed. If you are seeing
    this error, please see the note printed at the beginning of this script.\n
    """)
