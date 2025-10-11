import { Send, Paperclip, Smile } from "lucide-react";
import useChat from "../../hooks/chat/useChat.ts";

import {useEffect, useState} from "react";
import {apiConversation} from "../../services/api.ts";

const ChatArea = ({ activeChat }) => {
console.log('activechat', activeChat)

    const [conversationId, setConversationId] = useState<string | null>(null)


    useEffect(() => {

        if (!activeChat) return
        if ('unread' in activeChat){
            setConversationId(activeChat.id)
        }
        else if ('nickname' in activeChat){


            (async ()=>{
                const response = await apiConversation(activeChat.contact_user)
               setConversationId(response.conversationId)

            })()

        }
    }, [activeChat]);





const {messages} = useChat(conversationId)

    console.log('messages', messages)


  if (!activeChat) {
    return (
      <div
        className="flex-1 flex items-center justify-center"
        style={{
          backgroundImage:
            "url('https://telegram.org/img/tl_background_pattern.png'), linear-gradient(to top left, #e0fdd7, #a3d9c9)",
          backgroundBlendMode: "overlay",
          backgroundSize: "cover",
        }}
      >
        <p className="text-gray-500">یک مخاطب را انتخاب کنید</p>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col bg-white">
      {/* هدر چت */}
      <div className="p-3 border-b border-gray-300 flex items-center">
        <img
          src={activeChat.avatar}
          alt={activeChat.name}
          className="w-10 h-10 rounded-full mr-3"
        />
        <div className="flex-1">
          <h3 className="font-semibold">{activeChat.name}</h3>
          <p className="text-xs text-gray-500">آنلاین</p>
        </div>
      </div>

      {/* منطقه نمایش پیام‌ها */}
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
        <div className="space-y-4">
          {messages?.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.isMe ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-2xl ${
                  message.isMe
                    ? 'bg-blue-500 text-white rounded-br-none'
                    : 'bg-white text-gray-800 rounded-bl-none border border-gray-200'
                }`}
              >
                <p className="text-sm">{message.text}</p>
                <p className={`text-xs mt-1 ${message.isMe ? 'text-blue-100' : 'text-gray-500'} text-left`}>
                  {message.created_at}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* نوار تایپ پیام */}
      <div className="p-3 border-t border-gray-300">
        <div className="flex items-center">
          <button className="p-2 text-gray-500 hover:text-gray-700">
            <Paperclip size={20} />
          </button>
          <input
            type="text"
            placeholder="Type a message..."
            className="flex-1 mx-2 px-4 py-2 rounded-full bg-gray-100 focus:outline-none"
          />
          <button className="p-2 text-gray-500 hover:text-gray-700">
            <Smile size={20} />
          </button>
          <button className="ml-2 p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600">
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatArea;