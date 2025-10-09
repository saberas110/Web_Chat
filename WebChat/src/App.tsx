import './App.css'
import {Route, Routes} from "react-router-dom";
import AuthApp from "./ pages/register/AuthApp.tsx";
import Home from "./ pages/home/Home.tsx";
import ChatProvider from "./context/ChatContext.tsx";


function App() {


    return (
        <>
            <ChatProvider>
                <Routes>
                    <Route path='/' element={<AuthApp/>}/>
                    <Route path='/home' element={<Home/>}/>
                </Routes>
            </ChatProvider>
        </>
    )
}

export default App
