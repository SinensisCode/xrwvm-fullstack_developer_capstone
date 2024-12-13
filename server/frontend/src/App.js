import LoginPanel from "./components/Login/Login"
import Register from "./components/Register/Register";
import { Routes, Route } from "react-router-dom";
import Dealers from "./components/Dealers/Dealers";
import Dealer from "./components/Dealers/Dealer";
import HomePage from "./components/HomePage";

function App() {
  return (
     <div>
      <Routes>
        {/* Qui definisci la rotta per la home page */}
        <Route path="/" element={<HomePage />} />
        {/* Altri percorsi potrebbero essere aggiunti in seguito */}
    <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dealers" element={<Dealers />} />
      <Route path="/dealer/:id" element={<Dealer />} />
      </Routes>
    </div>
  );


}
export default App;
