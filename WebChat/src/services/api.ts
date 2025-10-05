import axios  from 'axios'


const accountHost = 'http://localhost:8000/accounts/'


function getCookie(name: string):string | null {
    const value = `;${document.cookie}`
    const parts = value.split(`; ${name}=`)
    if (parts.length == 2) return parts.pop()!.split(';').shift() || null
    return null
}


const account = axios.create({
    baseURL: accountHost,
    withCredentials: true
})



export async function getCSRFToken():Promise<string | null> {
    try {
        const response = await account.get('csrf')
        return response.data?.csrfToken || getCookie('csrftoken')
    }catch (error){
         console.error("Error getting CSRF token:", error);
    return null;
    }

}

account.interceptors.request.use(async (config) => {
  // اگر درخواست خودِ csrf هست، کاری نکن
  if (config.url?.includes("csrf")) {
    return config;
  }

  let csrfToken = getCookie("csrftoken");

  if (!csrfToken) {
    csrfToken = await getCSRFToken();
  }

  if (csrfToken) {
    config.headers["X-CSRFToken"] = csrfToken;
  }

  return config;
});

export async function apiOtp(phone:string){
  try {
    const response = await account.post("otp", {
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
        const response = await account.post('register', {
            'otp_code':otp
        })
        return response.data
    }catch (error){
        console.error("Error sending OTP:", error.response || null);
    throw error;
    }
}


