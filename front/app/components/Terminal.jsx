"use client"; // 클라이언트 컴포넌트로 지정

import { useEffect, useRef, useState } from 'react';
import Button from "@mui/material/Button";
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';

const TerminalComponent = () => {
  const terminalRef = useRef(null);
  const wsRef = useRef(null); // WebSocket 인스턴스를 저장할 ref
  const [step, setStep] = useState("");

  const initializeTerminal = async () => {
    const { Terminal } = await import('xterm');
    const { FitAddon } = await import('xterm-addon-fit');
    await import('xterm/css/xterm.css');

    const term = new Terminal({
      fontSize: 9
      ,lineHeight: 1.3
    });
    const fitAddon = new FitAddon();
    term.loadAddon(fitAddon);
    term.open(terminalRef.current);

    const res = await fetch('/api/generateProxyUrl', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include'
    })

    const ws = new WebSocket((await res?.json()).url);
    wsRef.current = ws;

    ws.onopen = () => {
      ws.send("clear\r");
      term.onData((data) => {
        ws.send(data);
      });

      ws.onmessage = (event) => {

        if(event.data.includes("메뉴 선택:")){
          setStep("SelectMenu");
        } else if(event.data.includes("열차 선택:")){
          setStep("SelectTrain");
        } else if(event.data.includes("SRT 계정 아이디:")){
          setStep("SetSRTID");
        } else if(event.data.includes("SRT 계정 패스워드:")){
          setStep("SetSRTPwd");
        } else if(event.data.includes("출발역 선택:")){
          setStep("SelectStart");
        } else if(event.data.includes("도착역 선택:")){
          setStep("SelectEnd");
        } else if(event.data.includes("출발 날짜 선택:")){
          setStep("SelectDate");
        } else if(event.data.includes("출발 시각 선택:")){
          setStep("SelectTime");
        } else if(event.data.includes("승객수:")){
          setStep("SelectPassenger");
        } else if(event.data.includes("예약할 열차 선택")){
          setStep("SelectTicket");
        } else if(event.data.includes("선택 유형:")){
          setStep("SelectSeatType");
        } else if(event.data.includes("예매 시 카드 결제")){
          setStep("SetPayYn");
        } else if(event.data.includes("KTX 계정 아이디")){
          setStep("SetKTXID");
        } else if(event.data.includes("KTX 계정 패스워드")){
          setStep("SetKTXPassword");
        } else if(event.data.includes("텔레그램")){
          setStep("SetTelegram");
        } else if(event.data.includes("신용카드 번호")){
          setStep("SetCard");
        } else if(event.data.includes("카드 비밀번호 앞 2자리")){
          setStep("SetCardPwd2");
        } else if(event.data.includes("생년월일")){
          setStep("SetCardBirth");
        } else if(event.data.includes("카드 유효기간")){
          setStep("SetCardExiredDate");
        } else if(event.data.includes("역 선택")){
          setStep("SetAvailableStation");
        } else if(event.data.includes("역 수정")){
          setStep("UpdAvailableStation");
        } else if(event.data.includes("예매 옵션 선택")){
          setStep("SetOptionsPassenger");
        } 
        term.write(event.data);
      };
    };

    return () => {
      term.dispose();
      ws.close();
    };
  };

  useEffect(() => {
    initializeTerminal();
  }, []);

  // 방향키 버튼 핸들러
  const handleArrowKey = (keyCode) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(keyCode); // 키 코드 전송
    }
  };

  return (
    <div style={{ display:'flex', flexDirection: 'column',width:'100%', height: '100%'}}>
      {/* 터미널 영역 */}
      <div ref={terminalRef} style={{ whiteSpace:'pre', width:'100%' }} />
      <div style={{display:'flex',justifyContent:'center',alignContent:'center', flexDirection: 'column', height: '100%'}}>
        <div style={{display:'flex', width:'100vw', flexDirection:'column', height: '100%' }}>
          <div style={{display:'flex', marginLeft:'auto'}}>
            <div>
              <Button onClick={() => handleArrowKey('N')} style={{visibility:step=="SetPayYn"?"visible":"hidden", color:'rgba(25,118,210,1)', fontWeight:'bold', background:'rgba(50,50,255,0.1)', marginTop:'53px',marginRight:'20px', borderRadius: '20px'}}>N</Button>
              <Button onClick={() => handleArrowKey('Y')} style={{visibility:step=="SetPayYn"?"visible":"hidden", color:'rgba(25,118,210,1)', fontWeight:'bold', background:'rgba(50,50,255,0.1)', marginTop:'53px',marginRight:'20px', borderRadius: '20px'}}>Y</Button>
            </div>
            <div>
              <Button onClick={() => handleArrowKey(' ')} style={{ visibility:step=="SelectTicket"||step=="SetAvailableStation"||step=="SetOptionsPassenger"?'visible':'hidden' ,color:'rgba(25,118,210,1)', fontWeight:'bold', background:'rgba(50,50,255,0.1)', marginTop:'53px',marginRight:'20px', borderRadius: '20px'}}>체크</Button>
            </div>
            <div style={{display:'flex',flexDirection:'column', marginLeft:'auto', marginRight:'10px', marginTop: '20px', gap:'10px'}}>
              <div style={{display:'flex', alignItems:'center',justifyContent:'center', background:'rgba(50,50,255,0.1)', borderRadius: '20px'}}><Button style={{ borderRadius: '20px'}} onClick={() => handleArrowKey('\x1b[A')}><KeyboardArrowUpIcon fontSize='large' /></Button></div>
              <div style={{display:'flex', alignItems:'center',justifyContent:'center', background:'rgba(50,50,255,0.1)', borderRadius: '20px'}}><Button style={{ borderRadius: '20px'}} onClick={() => handleArrowKey('\x1b[B')}><KeyboardArrowDownIcon fontSize='large' /></Button></div>
            </div>
          </div>

          <Button onClick={() => handleArrowKey('\r')} style={{color:'rgba(25,118,210,1)', fontWeight:'bold', background:'rgba(50,50,255,0.1)',marginTop:'100px', borderRadius: '20px'}}>다음</Button>
        </div>
      </div>
    </div>
  );
};
export default TerminalComponent;