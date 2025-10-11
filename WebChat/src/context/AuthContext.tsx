import React, {createContext, useContext, useEffect, useState} from "react";
import {apiOtp, apiUser} from "../services/api.ts";

interface IAuthProviderProps{
    children: React.ReactNode
}

interface IUser{
    phone_number:string
}


interface IAuthContext{
    user: IUser | null,
    lodding: boolean,



}



export const AuthContext = createContext({} as IAuthContext)

export const useAuthContext = ()=>{
    return useContext(AuthContext)
}


export default function AuthProvider({children}:IAuthProviderProps) {

    const [user, setUser] = useState(null)
    const [lodding, setLodding] = useState(true)

    useEffect(() => {
        const getUser = async () =>{
            try{
                const res = await  apiUser()
                setUser(res)
            }catch (error){
                console.log('get user error is :', error)
            }finally {
                setLodding(false)
            }
        }
        getUser()
    }, []);









    return (
        <AuthContext.Provider value={{user, lodding}}>


            {children}

        </AuthContext.Provider>

    )

}