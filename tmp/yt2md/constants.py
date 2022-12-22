obsidian_template = """\
# Video Name: %title

![[%video_file]]

#### [Link auf Youtube](%youtube_link)
#### [[%comments]]
[[Youtube Channel %channel_id]]

# Beschreibung

%description


# Notes


#youtubevideo 

~~~~~~~~~~~~~~~~~~~~~~~~~~
Retrieved: %downloaded_date
Views: %view_count
~~~~~~~~~~~~~~~~~~~~~~~~~~

# Transcript (Not Proofread)

%transcript

\
"""


resolution_levels = [2160, 1440, 1080, 720, 480, 360, 240, 144]
