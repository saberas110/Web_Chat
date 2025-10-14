import './App.css'
import {Route, Routes} from "react-router-dom";
import AuthApp from "./ pages/register/AuthApp.tsx";
import Home from "./ pages/home/Home.tsx";
import ChatProvider from "./context/ChatContext.tsx";
import AuthProvider from "./context/AuthContext.tsx";


function App() {


    return (
        <>

         <AuthProvider>
                <ChatProvider>
                <Routes>
                    <Route path='/' element={<AuthApp/>}/>
                    <Route path='/home' element={<Home/>}/>
                </Routes>
            </ChatProvider>
         </AuthProvider>


        </>
    )
}

export default App
