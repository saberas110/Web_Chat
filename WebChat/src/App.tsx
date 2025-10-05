import './App.css'
import {Route, Routes} from "react-router-dom";
import AuthApp from "./ pages/register/AuthApp.tsx";
import Home from "./ pages/home/Home.tsx";


function App() {


    return (
        <>
            <Routes>
                <Route path='/' element={<AuthApp />}/>
                <Route path='/home' element={<Home/>} />
            </Routes>
        </>
    )
}

export default App
