import React, {createContext, useContext, useEffect, useState} from "react";
import {apiChatList} from "../services/api.ts";

interface IchatProviderProps{
    children : React.ReactNode
}

interface IChatList{
    id: number,
    name: string,
    lastMessage: string
    time: string,
    unread: number,
    avatar: string

}


interface IChatContex{
    chatList: IChatList
}





const chatContext = createContext({} as IChatContex)

export const useChatContext = ()=>useContext(chatContext)



export default function ChatProvider({children}:IchatProviderProps){

    const [chatList, setChatList] = useState()



    useEffect(() => {
        console.log('start api')
        apiChatList().then(res=>{
            setChatList(res)
        })
    }, []);





    return(
        <chatContext.Provider value={{chatList, }}>

            {children}

        </chatContext.Provider>
    )
}