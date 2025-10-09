import axios  from 'axios'
import CSRFInteceptors from "./requestInterceptors.ts";
import RefreshInterceptors from "./requestInterceptors.ts";


const Host = 'http://localhost:8000/'

function getCookie(name: string):string | null {
    const value = `;${document.cookie}`
    const parts = value.split(`; ${name}=`)
    if (parts.length == 2) return parts.pop()!.split(';').shift() || null
    return null
}


const api = axios.create({
    baseURL: Host,
    withCredentials: true,
})

CSRFInteceptors(api)
RefreshInterceptors(api)





export async function apiOtp(phone:string){
  try {
    const response = await api.post("accounts/otp", {
        'phone':phone
    });
    return response.data;
  } catch (error: any) {
    console.error("Error sending OTP:", error.response || null);
    throw error;
  }
}

export async function apiRegister(otp:string){
    try{
        const response = await api.post('accounts/register', {
            'otp_code':otp
        })
        return response.data
    }catch (error){
        console.error("Error sending OTP:", error.response || null);
    throw error;
    }
}





export async function apiChatList(){
    console.log('start request for chatlist')
    try {
        const response =await api.get('chat/cvs')
        return response.data
    }catch (error){
        console.error("Error sending OTP:", error.response || null)
        throw error
    }
}



