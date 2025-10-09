import React, {createContext, useContext, useState} from "react";

interface IAuthProviderProps{
    children: React.ReactNode
}

interface IAuthContext{



}



export const AuthContext = createContext()

export const useAuthContext = ()=>{
    return useContext(AuthContext)
}


export default function AuthProvider({children}:IAuthProviderProps) {

    const [userInformations, setUserInformations] = useState(null)








    return (
        <AuthContext.Provider value={{}}>


            {children}

        </AuthContext.Provider>

    )

}