

on node 192.168.153.177

ffserver.conf
```
HTTPPort 1234
RTSPPort 1235

<Feed feed1.ffm>
        File /tmp/feed1.ffm
        FileMaxSize 2M
        ACL allow 127.0.0.1
</Feed>

<Stream test1.sdp>
    Feed feed1.ffm
    Format rtp
    Noaudio
    VideoCodec libx264
    AVOptionVideo flags +global_header
    AVOptionVideo me_range 16
    AVOptionVideo qdiff 4
    AVOptionVideo qmin 10
    AVOptionVideo qmax 51
</Stream>
```


```
ffserver -f ffserver.conf
```

ffmpeg push localfile to ffserver
```
ffmpeg -i source.200kbps.768x320.flv -vcodec libx264 -tune zerolatency -crf 18 http://localhost:1234/feed1.ffm
```

we get 
```
rtsp://192.168.153.177:1235/test1.sdp
```

open in vlc

