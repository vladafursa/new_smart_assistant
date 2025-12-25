import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Storage from "./pages/Storage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/storage" element={<Storage />} />
      </Routes>
    </BrowserRouter>
  );
}
