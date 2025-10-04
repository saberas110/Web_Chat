import './App.css'
import {Route, Routes} from "react-router-dom";
import AuthApp from "./ pages/register/AuthApp.tsx";


function App() {


    return (
        <>
            <Routes>
                <Route path='/' element={<AuthApp />}/>

            </Routes>
        </>
    )
}

export default App
