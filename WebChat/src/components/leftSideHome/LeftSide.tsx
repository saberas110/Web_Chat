import { useState } from "react";
import { Menu } from "lucide-react";
import {useChatContext} from "../../context/ChatContext.tsx";


export default function LeftSide() {

  const {chatList} = useChatContext()
  console.log('im from leftside', chatList)
  const [selectedUser, setSelectedUser] = useState(null);

  return (
    <div className="h-screen w-screen flex ">
      {/* سمت چپ */}
      <div className="w-80 border-r border-gray-300 flex flex-col bg-white">
        {/* هدر سرچ */}
        <div className="p-3 flex items-center">
          <button className="mr-2 p-2 hover:bg-gray-200 rounded-full">
            <Menu size={20} />
          </button>
          <input
            type="text"
            placeholder="Search"
            className="flex-1 px-4 py-2 rounded-full bg-gray-100 focus:outline-none"
          />
        </div>

        {/* لیست کاربران */}
        <div className="flex-1 overflow-y-auto">
          {chatList?.map((user) => (
            <div
              key={user.id}
              onClick={() => setSelectedUser(user.id)}
              className={`flex items-center p-3 cursor-pointer border-b border-gray-200
                ${selectedUser === user.id ? "bg-gray-100" : "hover:bg-gray-50"}`}
            >
              <img
                src={user.avatar}
                alt={user.name}
                className="w-12 h-12 rounded-full mr-3"
              />
              <div className="flex-1">
                <div className="flex justify-between items-center">
                  <h2 className="font-semibold text-sm">{user.name}</h2>
                  <span className="text-xs text-gray-500">{user.time}</span>
                </div>
                <div className="flex justify-between items-center">
                  <p className="text-sm text-gray-600 truncate max-w-[160px]">
                    {user.last_message}
                  </p>
                  {user.unread > 0 && (
                    <span className="ml-2 bg-green-500 text-white text-xs px-2 py-0.5 rounded-full">
                      {user.unread}
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* سمت راست */}
      <div
        className="flex-1 flex items-center justify-center"
        style={{
          backgroundImage:
            "url('https://telegram.org/img/tl_background_pattern.png'), linear-gradient(to top left, #e0fdd7, #a3d9c9)",
          backgroundBlendMode: "overlay",
          backgroundSize: "cover",
        }}
      >
        {selectedUser ? (
          <p className="text-gray-600">
            در حال چت با {chatList.find((u) => u.id === selectedUser)?.name}
          </p>
        ) : (
          <p className="text-gray-500">یک مخاطب را انتخاب کنید</p>
        )}
      </div>
    </div>
  );
}
