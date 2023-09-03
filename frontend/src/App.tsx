import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Narrration from './pages/Narration';
import Home from './pages/Home';
import Notes from './pages/Notes';
import SignLanguage from './pages/SignLanguage';
import Navbar from './components/Navbar';
import About from './pages/About';
import Braille from './pages/Braille';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route index element={<Home />} />
          <Route path="about" element={<About />} />
          <Route path="notes" element={<Notes />} />
          <Route path="narration" element={<Narrration />} />
          <Route path="sign" element={<SignLanguage />} />
          <Route path="braille" element={<Braille />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
