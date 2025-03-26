"use client"
import TextField from '@mui/material/TextField';
import Button from "@mui/material/Button";
import { useState } from 'react';
import { toast } from 'react-toastify'

const Index = () => {
    const [password, setPassword] = useState("");

    const keyDownHandler = (e) => {
        if (e.code == "Enter") {
            checkPassword(e?.target?.value)
        }
    }

    const onChangeHandler = (e) => {
        setPassword(e?.target?.value);
    }

    const checkPassword = async (pwd) => {
        const res = await fetch('/api/check-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: pwd }),
            credentials: 'include'
        })

        if (res.redirected) {
            toast.success('Success Login')
            // 리디렉트 URL로 강제 이동
            window.location.href = res.url
            return
        }

        const data = await res.json()

        if (!data.valid) {
            toast.error('비밀번호 오류')
        }
    }


    return (
        <div style={{ width: '100vw', height: '100vh', background: '#222', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <TextField
                label="Password"
                type="password"
                autoComplete="current-password"
                variant="filled"
                onKeyDown={keyDownHandler}
                onChange={onChangeHandler}
                sx={{
                    '& label': {
                        color: 'white'
                    },
                    '& label.Mui-focused': {
                        color: 'white'
                    },
                    '& .MuiInput-underline:after': {
                        borderBottomColor: 'white',
                    },
                    background: '#404040'
                    , color: 'white'
                    , input: {
                        color: 'white', // ● 색상 변경
                    }
                    , height: '50px'
                    , width: '45%'
                }}
            />

            <Button sx={{width: '5%', height:'50px', marginLeft:'1rem', background:'#D9D9D9', color: '#222'}} onClick={()=>{checkPassword(password)}}>확인</Button>
        </div>
    )
}

export default Index;