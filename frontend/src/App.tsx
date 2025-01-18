// import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './login/page';
import { Connexion } from './components/connexion';
function App() {
  return (
    <Router>
      <div className="flex h-screen justify-center items-center">
        <Routes>
          <Route
            path="/"
            element={
              <div className="">
                <LoginPage />
              </div>
            }
          />
          <Route
            path="/test"
            element={
              <div className="">
                <Connexion />
              </div>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;