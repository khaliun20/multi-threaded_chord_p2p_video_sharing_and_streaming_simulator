# Play a video stored on a distributed Chord network!

The user needs to run three processes. Process 1 implements port-forwarding from the Chord network to the video player. We found we had to do this because we implemented Chord using TCP sockets, but the video player uses a React websocket. Process 2 runs the video player. Process 3 initializes the Chord network, and sets up the nodes to continually listen to one another and find files in Chord in log(N) time. CLI commands are as follows:

**Process 1: Port Forwarding between 2 and 3**
`python -m src.Chord.video_upload`

**Process 2: Run the React Video Player**
`cd video-player`
`npm start`

**Process 3: Initialize the Chord Network**
`python -m src.Chord.network`
