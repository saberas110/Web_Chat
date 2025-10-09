import {useEffect} from "react";
import {data} from "react-router";

const WS_URL:string = 'ws://localhost:8000/ws/presence/'

export default function usePresence(){

    useEffect(()=>{
        const ws = new WebSocket(WS_URL)

        ws.onopen = ()=> console.log("presence websocket opened")
        ws.onmessage = (ev)=>{
            const data = JSON.parse(ev.data)
            console.log('presence ev: ', data)
        }

        return ()=> {
            ws.onclose = (ev)=>{
                ws.close()
            //    const data = JSON.parse(ev.data)
            // console.log('presence ev: ', data)
            }
        }



    }, [])
}