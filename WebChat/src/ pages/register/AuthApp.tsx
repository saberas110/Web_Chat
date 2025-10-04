import {useState} from "react";
import PhoneLoginPage from './PhoneLoginPage'
import OTPLoginPage from './OTPLoginPage'

export default function AuthApp(){
  const [currentPage, setCurrentPage] = useState('phone'); // 'phone' یا 'otp'
  const [userPhone, setUserPhone] = useState('');

  const handlePhoneSubmit = (phone) => {
    setUserPhone(phone);
    setCurrentPage('otp');
    // در اینجا می‌توانید درخواست ارسال کد OTP به سرور را انجام دهید
    console.log('Phone submitted:', phone);
  };

  const handleOtpVerify = (otpCode) => {
    // در اینجا لاگین نهایی با OTP را انجام دهید
    console.log('OTP verified:', otpCode);
    console.log('User phone:', userPhone);
    // پس از موفقیت آمیز بودن لاگین، کاربر را به صفحه اصلی هدایت کنید
  };

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
