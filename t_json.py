import json

jtext= ''' 
{
    "streams": [
        {
            "index": 0,
            "codec_name": "hevc",
            "codec_long_name": "H.265 / HEVC (High Efficiency Video Coding)",
            "profile": "Main",
            "codec_type": "video",
            "codec_time_base": "1/50",
            "codec_tag_string": "[0][0][0][0]",
            "codec_tag": "0x0000",
            "width": 1920,
            "height": 1080,
            "coded_width": 1920,
            "coded_height": 1088,
            "has_b_frames": 0,
            "sample_aspect_ratio": "1:1",
            "display_aspect_ratio": "16:9",
            "pix_fmt": "yuv420p",
            "level": 123,
            "color_range": "tv",
            "refs": 1,
            "r_frame_rate": "50/1",
            "avg_frame_rate": "50/1",
            "time_base": "1/1000",
            "start_pts": 0,
            "start_time": "0.000000",
            "disposition": {
                "default": 1,
                "dub": 0,
                "original": 0,
                "comment": 0,
                "lyrics": 0,
                "karaoke": 0,
                "forced": 0,
                "hearing_impaired": 0,
                "visual_impaired": 0,
                "clean_effects": 0,
                "attached_pic": 0,
                "timed_thumbnails": 0
            },
            "tags": {
                "ENCODER": "Lavc58.66.100 hevc_nvenc",
                "DURATION": "01:28:50.120000000"
            }
        },
        {
            "index": 1,
            "codec_name": "aac_latm",
            "codec_long_name": "AAC LATM (Advanced Audio Coding LATM syntax)",
            "profile": "LC",
            "codec_type": "audio",
            "codec_time_base": "1/48000",
            "codec_tag_string": "[2][22][0][0]",
            "codec_tag": "0x1602",
            "sample_fmt": "fltp",
            "sample_rate": "48000",
            "channels": 6,
            "channel_layout": "5.1",
            "bits_per_sample": 0,
            "r_frame_rate": "0/0",
            "avg_frame_rate": "0/0",
            "time_base": "1/1000",
            "start_pts": 85,
            "start_time": "0.085000",
            "disposition": {
                "default": 1,
                "dub": 0,
                "original": 0,
                "comment": 0,
                "lyrics": 0,
                "karaoke": 0,
                "forced": 0,
                "hearing_impaired": 0,
                "visual_impaired": 0,
                "clean_effects": 0,
                "attached_pic": 0,
                "timed_thumbnails": 0
            },
            "tags": {
                "language": "deu",
                "DURATION": "01:28:50.005000000"
            }
        },
        {
            "index": 2,
            "codec_name": "aac_latm",
            "codec_long_name": "AAC LATM (Advanced Audio Coding LATM syntax)",
            "profile": "LC",
            "codec_type": "audio",
            "codec_time_base": "1/48000",
            "codec_tag_string": "[2][22][0][0]",
            "codec_tag": "0x1602",
            "sample_fmt": "fltp",
            "sample_rate": "48000",
            "channels": 2,
            "channel_layout": "stereo",
            "bits_per_sample": 0,
            "r_frame_rate": "0/0",
            "avg_frame_rate": "0/0",
            "time_base": "1/1000",
            "start_pts": 85,
            "start_time": "0.085000",
            "disposition": {
                "default": 1,
                "dub": 0,
                "original": 0,
                "comment": 0,
                "lyrics": 0,
                "karaoke": 0,
                "forced": 0,
                "hearing_impaired": 0,
                "visual_impaired": 0,
                "clean_effects": 0,
                "attached_pic": 0,
                "timed_thumbnails": 0
            },
            "tags": {
                "language": "mis",
                "DURATION": "01:28:50.005000000"
            }
        }
    ]
}
'''

inhalt = json.loads(jtext)

# print(inhalt[0])


print(inhalt['streams'][0]["codec_type"])
print(inhalt['streams'][0]["codec_name"])
print(str(inhalt['streams'][0]["width"]) + "x" + str(inhalt['streams'][0]["height"]))

print(inhalt['streams'][1]["codec_type"])
print(inhalt['streams'][1]["codec_name"])
print(str(inhalt['streams'][1]["channel_layout"]) + " / " + str(inhalt['streams'][1]["tags"]["language"]))

lfdnr = 0
for stream in inhalt['streams']:
    print(lfdnr, end= ": ")
    print(stream["codec_type"] , end=" ") 
    print(stream["codec_name"]) + " (" + stream["codec_name"])
    lfdnr +=1
    