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
                console.log('chat messages:', data.messages)
                setMessages(data.messages)
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
            ws.close();
        }


    }, [conversationId]);

return {messages}
}