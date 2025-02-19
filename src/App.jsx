import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import UploadFiles from './Components/UploadFiles'
import Report from './Components/Report'

function App() {

  return (
    <Routes>
      <Route path="/report" element={<Report />} />
      <Route path="/" element={<UploadFiles />} />
    </Routes>
  )
}

export default App
