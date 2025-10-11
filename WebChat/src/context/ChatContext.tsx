import React, {createContext, useContext, useEffect, useState} from "react";
import {apiChatList, apiContacts, apiConversation} from "../services/api.ts";
import {useAuthContext} from "./AuthContext.tsx";

interface IchatProviderProps {
    children: React.ReactNode
}

interface IChatList {
    id: number,
    name: string,
    lastMessage: string
    time: string,
    unread: number,
    avatar: string

}

interface IContacts {
    id: number,
    contact_user: string,
    nickname: string,
    last_seen: string,
    is_online: boolean,
    avatar: string
}


interface IChatContex {
    chatList: IChatList[],
    contacts: IContacts[],
    getConversationId: (id:string)=>Promise<string>
}


const chatContext = createContext({} as IChatContex)

export const useChatContext = () => useContext(chatContext)


export default function ChatProvider({children}: IchatProviderProps) {
    const {user, lodding} = useAuthContext()
    const [chatList, setChatList] = useState<IChatList[]>([])
    const [messages, setMessages] = useState()
    const [contacts, setContacts] = useState<IContacts[]>([])
    const [conversationId, setConversationId] = useState<string | null>(null)


    useEffect(() => {
        if (!lodding){
            apiChatList().then(setChatList)
            apiContacts().then(setContacts)
        }
    }, [lodding]);


async function getConversationId(id:string){
    await apiConversation(id).then(res=>{
        setConversationId(res)
    })
    return res
}


        return (
            <chatContext.Provider value={{chatList, contacts, getConversationId}}>

                {children}

            </chatContext.Provider>
        )
    }