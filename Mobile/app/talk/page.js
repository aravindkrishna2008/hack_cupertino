"use client";
import { useSpeechSynthesis } from "react-speech-kit";
import { useEffect } from "react";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
  
const MyComponent = () => {
  const { speak, voices } = useSpeechSynthesis();
    useEffect(() => {
        console.log("speak")
        handleSpeak("Ready to cross. Walk straight!")
    }
, []);
  const handleSpeak = (text) => {
    console.log("speaking");
    const voiceToUse = voices[1]; // You can choose a specific voice if desired
    speak({ text: text, voice: voiceToUse });
    sleep(1000);
    speak({ text: text, voice: voiceToUse });
    sleep(1000);

    speak({ text: text, voice: voiceToUse });
    sleep(1000);

    speak({ text: text, voice: voiceToUse });
    sleep(1000);

    speak({ text: text, voice: voiceToUse });
    sleep(1000);

    speak({ text: text, voice: voiceToUse });
    sleep(1000);

    speak({ text: text, voice: voiceToUse });
    sleep(1000);

    speak({ text: text, voice: voiceToUse });
  };

  return (
    <div>
      <button onClick={() => handleSpeak("Ready to cross. Walk straight!")}>
        Spesak
      </button>
    </div>
  );
};

export default MyComponent;
