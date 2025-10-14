import {useEffect, useRef, useState} from "react";


export default function useChat(conversationId) {
    const wsRef = useRef<WebSocket | null>(null);

    const [messages, setMessages] = useState()

    console.log('im from usechat', conversationId)

    useEffect(() => {

        if (!conversationId) return;

         const WS_URL = `ws://localhost:8000/ws/chat/${conversationId}/`

        const ws = new WebSocket(WS_URL)
        wsRef.current = ws

        ws.onopen = () => console.log('open ws chat for :', conversationId)

        ws.onmessage = (event) => {



            try {
                const data = JSON.parse(event.data)

                if (data.type==='init_message'){
                       setMessages(data.messages)
                }else if (data.type==='new_message'){
                    console.log('new_message', data)
                    setMessages(prevState => [...prevState, data.message])
                }

            } catch (err) {
                console.log('error is :', err)
            }
        }

        ws.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        ws.onclose = (event) => {
            console.log('socket closed:', event.code, event.reason)
        }

        return () => {
            console.log("Closing old chat socket...");
            wsRef.current?.close()
        }



    }, [conversationId]);

    const sendMessage = (text:string)=>{
        const ws = wsRef.current
        if(!ws){
            console.warn('WebSocket not connected yet!')
            return
        }
        if (ws.readyState === WebSocket.OPEN){
            const messageData = {
                type: "chat_message",
                messages: text
            }
            ws.send(JSON.stringify(messageData))
            console.log("Message Sent:", messageData)
        }else {
            console.warn("WebSocket is not open:", ws.readyState)
        }
    }

return {messages, sendMessage}
}