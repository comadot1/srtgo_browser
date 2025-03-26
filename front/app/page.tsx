"use client"
import TerminalComponent from './components/Terminal';

export default function Home() {
  return (
    <div style={{display:'flex', flexDirection:'column', width: "100%", flex:1, height:'100vh'}}>
      <TerminalComponent />
    </div>
  );
}