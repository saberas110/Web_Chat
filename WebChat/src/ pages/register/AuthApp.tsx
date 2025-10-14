import {useState} from "react";
import PhoneLoginPage from './PhoneLoginPage'
import OTPLoginPage from './OTPLoginPage'
import {apiOtp, apiRegister} from "../../services/api.ts";
import {useNavigate} from "react-router";
import useChatList from "../../hooks/chat/useChatList.tsx";


export default function AuthApp(){
  const {chatList} = useChatList()
  const [currentPage, setCurrentPage] = useState('phone'); // 'phone' یا 'otp'
  const [userPhone, setUserPhone] = useState('');
  const navigate = useNavigate()

  console.log('chatList', chatList)


  const handlePhoneSubmit = async (phone) => {
    setUserPhone(phone);
    await apiOtp(phone).then(res=>{
      console.log('response is ', res)
      setCurrentPage('otp');
    })
  };

  const handleOtpVerify = async (otpCode) => {
    await apiRegister(otpCode).then(res=>{
      console.log('response is ', res)
      navigate('/home')
    })

    }




  const handleBackToPhone = () => {
    setCurrentPage('phone');
    setUserPhone('');
  };

  return (
    <>
      {currentPage === 'phone' && (
        <PhoneLoginPage onPhoneSubmit={handlePhoneSubmit} />
      )}

      {currentPage === 'otp' && (
        <OTPLoginPage
          phoneNumber={userPhone}
          onBack={handleBackToPhone}
          onVerify={handleOtpVerify}
        />
      )}
    </>
  );
};
