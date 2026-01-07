"use client"
import React, { useRef, useEffect, useState } from "react";
import { useSpeechSynthesis } from "react-speech-kit";


const VideoComponent = () => {
  const videoRef = useRef(null);
  const intervalRef = useRef(null);

  const [text, setText] = useState("Don't cross")

  const [counter, setCounter] = useState(0)

  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  const { speak, voices } = useSpeechSynthesis();

  const handleSpeak = (text) => {
    console.log("speaking");
    const voiceToUse = voices[1];
    speak({ text: text, voice: voiceToUse });
  };


  useEffect(() => {
    const start = () => {
      const video = document.createElement("video");
      video.src = "/IMG_0159.mp4";
      video.preload = "auto";
      video.loop = true;
      video.muted = true;
      video.play();

      video.addEventListener("loadeddata", () => {
        videoRef.current.srcObject = video.captureStream();
        intervalRef.current = setInterval(captureImage, 1000);
      });
    };

    start();

    return () => {
      clearInterval(intervalRef.current);
    };
  }, []);

const captureImage = async () => {
  const canvas = document.createElement("canvas");
  canvas.width = 1080;
  canvas.height = 1920;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);

  const imageData = canvas.toDataURL("image/jpeg");

  try {
    const formData = new FormData();
    formData.append("frame", imageData);

    const response = await fetch("http://172.16.20.76:846/api/process-frame", {
      method: "POST",
      body: formData,
    });

    response.json().then(
      (data) => {
        setText(data["light"])
      }
    )


    if (!response.ok) {
      throw new Error("Failed to upload image. Status: " + response.status);
    }


  } catch (error) {
    console.error("Error uploading image: ", error);
  }
};


  return (
    <div style={{width:"100%", height:"100%", backgroundColor:"black", paddingLeft:"5vw", paddingRight:"5vw"}}>
      {/* <div className="text-white absolute top-2 right-0 left-0 " style={{textAlign:"center"}}>
        <p  className="" style={{fontSize:"45px", fontWeight:"bold", fontStyle:"italic", color:"white"}}>CrossSight</p>
      </div> */}
      <img className="absolute top-6 left-9 right-0" style={{zIndex:1, width:"80vw", height:"8vh"}} src={"https://media.discordapp.net/attachments/1071229828319162429/1229067598541488139/Frame_3_1.png?ex=662e5566&is=661be066&hm=0988adb7401b06386882adc8e136b9039249e23414d8af8880667a0ff06bacdd&=&format=webp&quality=lossless&width=1440&height=307"}>
      </img>
      <br></br>
      <video className="h-[97vh]" autoPlay playsInline ref={videoRef} preload="auto" style={{borderRadius:"5%"}} loop controls>
      </video>
      <div className={`absolute bottom-20 p-2 mx-10 rounded-[20px] left-0 right-0 ${text == "Can cross" ? "bg-green-500" : "bg-red-500"} opacity-60`} style={{textAlign:"center"}}>
        <p className="text-white opacity-100" style={{fontSize:"40px", fontWeight:"bold"}}>{text}</p>
      </div>
      <button className="absolute top-[10vw] left-[10vw] h-[80vh] w-[80vw]" onClick={() => handleSpeak(text)} style={{backgroundColor:"transparent", color:"white", fontWeight:"bold", fontSize:"26px"}}>
        Click anywhere to read
      </button>
    </div>
  );
};

export default VideoComponent;
