"use client";

import {useEffect,useState} from "react";

type InstallEvent=Event&{prompt:()=>Promise<void>;userChoice:Promise<{outcome:"accepted"|"dismissed"}>};

export function PwaShell(){
  const [installEvent,setInstallEvent]=useState<InstallEvent|null>(null);
  const [offline,setOffline]=useState(false);

  useEffect(()=>{
    if("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");
    const update=()=>setOffline(!navigator.onLine);
    const capture=(event:Event)=>{event.preventDefault();setInstallEvent(event as InstallEvent)};
    update();
    window.addEventListener("online",update);
    window.addEventListener("offline",update);
    window.addEventListener("beforeinstallprompt",capture);
    return ()=>{window.removeEventListener("online",update);window.removeEventListener("offline",update);window.removeEventListener("beforeinstallprompt",capture)};
  },[]);

  async function install(){
    if(!installEvent)return;
    await installEvent.prompt();
    await installEvent.userChoice;
    setInstallEvent(null);
  }

  return <>
    {offline&&<div className="mobile-status-banner" role="status">Offline mode · saved pages remain available</div>}
    {installEvent&&<aside className="install-app-card">
      <img src="/shield-logo.svg" alt=""/>
      <span><b>Install Shield</b><small>Faster access from your home screen</small></span>
      <button onClick={install}>Install</button>
      <button aria-label="Dismiss install prompt" onClick={()=>setInstallEvent(null)}>×</button>
    </aside>}
  </>;
}
