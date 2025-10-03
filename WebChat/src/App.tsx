import './App.css'
import {Route, Routes} from "react-router-dom";
import Home from "./ pages/home/Home.tsx";


function App() {


    return (
        <>
            <Routes>
                <Route path='/' element={<Home />}/>
            </Routes>
        </>
    )
}

export default App
