import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import EarthDashBoard from "./pages/EarthDashBoard";
import MainPage from "./pages/MainPage";
import MarsDashBoard from "./pages/MarsDashBoard";

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/earthquake" element={<EarthDashBoard />} />
          <Route path="/marsquake" element={<MarsDashBoard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
