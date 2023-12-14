import './App.css';
import StreamingNav from "./components/navBar";
import Video from "./components/video";
import Dropdown from "./components/dropdown";
import VideoDisplay from "./components/videoDisplay";

function App() {

    return (
        <div className="App">
            <StreamingNav />
            {/*<Video />*/}
            <VideoDisplay />

        </div>
    );
}

export default App;
